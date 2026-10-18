<script>
/* 無料相談（2段階版）：1画面目の入力内容を、UTAGEの日時選択ページ（ut.exnet.biz）にだけ postMessage で渡す。URLには載せない */
(function(){var b=document.querySelector('[data-book]');if(!b)return;var O='https://ut.exnet.biz',SRC='%SRC%';
var st=b.querySelector('[data-book-step]'),who=b.querySelector('[data-book-who]'),fr=b.querySelector('[data-book-frame]'),rt=b.querySelector('[data-book-retry]'),data=null,done=false;
function ok(){var good=true;st.querySelectorAll('.field-err').forEach(function(e){e.remove()});
st.querySelectorAll('[required]').forEach(function(el){var v=el.value.trim(),bad=el.type==='checkbox'?!el.checked:!v,msg=el.type==='checkbox'?'同意いただくと進めます':el.tagName==='SELECT'?'選んでください':'入力してください';
if(!bad&&el.type==='email'&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)){bad=true;msg='メールアドレスの形をご確認ください';}
if(bad){good=false;var s=document.createElement('span');s.className='field-err';s.textContent=msg;el.closest('label').appendChild(s);}});
if(!good){var e=st.querySelector('.field-err');if(e)e.closest('label').scrollIntoView({block:'center'});}return good;}
function send(){if(data&&fr.contentWindow)fr.contentWindow.postMessage({type:'exnet-prefill',data:data},O);}
function step(two){st.hidden=two;who.hidden=!two;fr.hidden=!two;if(!two)rt.hidden=true;var r=b.getBoundingClientRect();if(r.top<0)b.scrollIntoView({block:'start'});}
b.querySelector('[data-book-next]').addEventListener('click',function(){if(!ok())return;data={};st.querySelectorAll('[name]').forEach(function(el){data[el.name]=el.value.trim()});
b.querySelector('[data-book-name]').textContent=data.sei+' '+data.mei+' 様（'+data.mail+'）';step(true);
if(!fr.getAttribute('src')){done=false;fr.setAttribute('src',SRC);setTimeout(function(){if(!done)rt.hidden=false;},10000);}else send();});
b.querySelector('[data-book-back]').addEventListener('click',function(){step(false)});
window.addEventListener('message',function(e){if(e.origin!==O||!e.data)return;var d=e.data;
if(d.type==='exnet-ready')send();else if(d.type==='exnet-height'&&d.h>200)fr.style.height=d.h+'px';else if(d.type==='exnet-prefill-done'){done=true;rt.hidden=!!d.ok;}});})();
</script>
