/**
 * exnet.biz 資料請求の受付（Google Apps Script のウェブアプリ）
 *
 * サイトの資料請求フォーム → このアプリ → UTAGE の流れで登録する。
 * UTAGE の受付先はこのアプリの設定（スクリプト プロパティ）にだけ置き、ページには出さない。
 *
 * スクリプト プロパティ（プロジェクトの設定 → スクリプト プロパティ）に入れるもの：
 *   RECAPTCHA_SECRET … reCAPTCHA のシークレットキー
 *   UTAGE_URL        … UTAGE の新しい資料請求シナリオの受付先（https://ut.exnet.biz/r/〇〇/store）
 *   ALERT_TO         … 見張りの知らせを送る先（info@exnet.biz）
 *
 * 確かめること（どれか1つでも引っかかったら UTAGE に送らない）：
 *   1. おとりの欄（ex_confirm）が空か
 *   2. 入力の形（必須・長さ・メールアドレス）
 *   3. お名前・会社名に URL や広告文がないか
 *   4. reCAPTCHA の点数（0.5 以上、action=download、ホスト exnet.biz）
 *   5. 1時間あたりの件数（4件目で ALERT_TO に知らせる、11件目からは受け付けない）
 */
var MIN_SCORE = 0.5;
var ALERT_AT = 4;     // 1時間でこの件数に達したら知らせる
var STOP_AT = 11;     // 1時間でこの件数からは受け付けない
var SPAM_WORDS = /(https?:|www\.|telegra|promo ?code|bonus ?code|\$\s?\d|\d\s?usd)/i;

function doPost(e) {
  var d;
  try { d = JSON.parse(e.postData.contents); } catch (err) { return out_({ ok: false, code: 'bad_request' }); }

  // 1. おとりの欄：埋まっていたら、送れたふりをして終える
  if (d.ex_confirm) { count_('hp'); return out_({ ok: true }); }

  // 2. 入力の形
  var name = String(d.name || '').trim();
  var mail = String(d.mail || '').trim();
  var company = String(d.company || '').trim();
  if (!name || !mail || !company || name.length > 60 || company.length > 100 ||
      !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail)) {
    return out_({ ok: false, code: 'invalid' });
  }

  // 3. 広告文
  if (SPAM_WORDS.test(name + ' ' + company)) { count_('words'); return out_({ ok: true }); }

  var props = PropertiesService.getScriptProperties();

  // 4. reCAPTCHA
  var v = {};
  try {
    v = JSON.parse(UrlFetchApp.fetch('https://www.google.com/recaptcha/api/siteverify', {
      method: 'post',
      payload: { secret: props.getProperty('RECAPTCHA_SECRET'), response: String(d.token || '') },
      muteHttpExceptions: true
    }).getContentText());
  } catch (err) { v = { success: false }; }
  if (!v.success || v.score < MIN_SCORE || v.action !== 'download' || (v.hostname && v.hostname !== 'exnet.biz')) {
    count_('captcha');
    console.log('captcha NG: success=' + v.success + ' score=' + v.score + ' action=' + v.action +
      ' hostname=' + v.hostname + ' errors=' + JSON.stringify(v['error-codes'] || []));
    return out_({ ok: false, code: 'captcha' });
  }

  // 5. 1時間あたりの件数
  var n = count_('ok');
  if (n === ALERT_AT) {
    alert_('資料請求が1時間に' + ALERT_AT + '件に達しました',
      '1時間に' + ALERT_AT + '件目の資料請求が入りました。ボットの可能性があります。\n' +
      'UTAGE の読者一覧を確認してください。1時間に' + STOP_AT + '件目からは自動で受付を止めます。\n\n' +
      '今回の内容：' + name + '／' + company + '／' + mail);
  }
  if (n >= STOP_AT) { return out_({ ok: false, code: 'busy' }); }

  // UTAGE に登録
  var res;
  try {
    res = UrlFetchApp.fetch(props.getProperty('UTAGE_URL'), {
      method: 'post',
      payload: { name: name, mail: mail, free93: company },
      followRedirects: false,
      muteHttpExceptions: true
    });
  } catch (err) {
    alert_('資料請求をUTAGEに登録できませんでした', String(err) + '\n\n' + name + '／' + company + '／' + mail);
    return out_({ ok: false, code: 'utage' });
  }
  var codeNum = res.getResponseCode();
  if (codeNum >= 400) {
    alert_('資料請求をUTAGEに登録できませんでした', 'UTAGE の応答：' + codeNum + '\n\n' + name + '／' + company + '／' + mail);
    return out_({ ok: false, code: 'utage' });
  }
  return out_({ ok: true });
}

// 動いているかの確認用（ブラウザでウェブアプリのURLを開くと表示される）
function doGet() {
  return out_({ ok: true, service: 'exnet.biz download intake' });
}

// 種類ごとに、この1時間の件数を数える
function count_(kind) {
  var lock = LockService.getScriptLock();
  lock.waitLock(5000);
  try {
    var cache = CacheService.getScriptCache();
    var key = kind + Utilities.formatDate(new Date(), 'Asia/Tokyo', 'yyyyMMddHH');
    var n = Number(cache.get(key) || 0) + 1;
    cache.put(key, String(n), 7200);
    return n;
  } finally {
    lock.releaseLock();
  }
}

function alert_(subject, body) {
  var to = PropertiesService.getScriptProperties().getProperty('ALERT_TO');
  if (to) MailApp.sendEmail(to, '【exnet.biz】' + subject, body);
}

function out_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
