export type ScamSignal={id:string;title:string;evidence:string;action:string;severity:'high'|'medium'|'info'};
// Fold Vietnamese accents for matching while preserving exact original evidence.
function searchable(input:string){let text='',offset=0;const starts:number[]=[],ends:number[]=[];for(const c of input){const f=c.normalize('NFD').replace(/[\p{M}\u200b-\u200d\ufeff]/gu,'').replace(/đ/gi,'d').toLowerCase();for(let j=0;j<f.length;j++){starts.push(offset);ends.push(offset+c.length);}text+=f;offset+=c.length;}return {text,evidence:(index:number,length:number)=>input.slice(starts[index],ends[index+length-1])};}
export function expectedHostname(input:string){if(!input.trim())return '';const raw=input.trim().replace(/^https?:\/\//i,'').replace(/\/$/,'');if(/[\s/@:#?\\]/.test(raw))throw Error('Nhập riêng tên miền chính thức, ví dụ example.com, không kèm đường dẫn.');let host='';try{host=new URL('https://'+raw).hostname.replace(/\.$/,'');}catch{throw Error('Tên miền đối chiếu không hợp lệ.');}if(!host.includes('.')||host.length>253||!/^[a-z0-9.-]+$/i.test(host)||host.split('.').some(s=>!s||s.startsWith('-')||s.endsWith('-')))throw Error('Tên miền đối chiếu không hợp lệ.');return host;}
export function inspectScam(input:string,expectedDomain=''){
 if(input.length>20000)throw Error('Tối đa 20.000 ký tự cho một lần kiểm tra.');
 const expected=expectedHostname(expectedDomain),signals:ScamSignal[]=[],urls:{url:string;host:string;matchesExpected?:boolean}[]=[];
 const add=(id:string,title:string,evidence:string,action:string,severity:ScamSignal['severity']='info')=>{if(!signals.some(s=>s.id===id&&s.evidence===evidence))signals.push({id,title,evidence:evidence.slice(0,240),action,severity});};
 const normalized=searchable(input);
 const rules:[string,RegExp,string,string,ScamSignal['severity']][]=[
  ['credentials',/(?:cung cap|gui|doc|nhap|cho xin|share|send|enter)[^.!?\n]{0,70}(?:\botp\b|ma xac (?:thuc|nhan)|mat khau|password|recovery phrase|seed phrase)/g,'Yêu cầu thông tin xác thực','Không cung cấp OTP, mật khẩu hoặc cụm khôi phục cho người liên hệ.','high'],
  ['advance-payment',/(?:chuyen (?:tien|khoan)|dong phi|nop phi|dat coc|transfer money)[^.!?\n]{0,100}(?:nhan (?:qua|thuong|tien)|mo khoa|xac minh|hoan tien)|(?:trung thuong|nhan qua)[^.!?\n]{0,100}(?:phi|chuyen khoan)/g,'Yêu cầu trả tiền để nhận lợi ích','Xác minh độc lập với tổ chức qua kênh chính thức trước khi giao dịch.','high'],
  ['urgency',/(?:khoa tai khoan|bat giu|phat tien|account suspended)[^.!?\n]{0,100}(?:ngay|khan|phut|gap|immediately)/g,'Gây áp lực phải hành động gấp','Dừng trao đổi và tự liên hệ tổ chức bằng số hoặc ứng dụng đã biết.','medium'],
  ['remote-app',/(?:cai|tai|install|download)[^!?\n]{0,80}(?:\.apk|anydesk|teamviewer|dieu khien tu xa)/g,'Đề nghị cài ứng dụng hoặc điều khiển từ xa','Không cấp quyền điều khiển từ tin nhắn chưa xác minh.','medium']
 ];
 for(const [id,rule,title,action,severity]of rules)for(const m of normalized.text.matchAll(rule)){
  const prefix=normalized.text.slice(Math.max(0,m.index!-45),m.index).split(/[.!?;,\n]/).at(-1)||'';
  // A direct safety instruction is not itself a request to surrender credentials.
  if(/\b(?:khong|dung|cho|never|do not|don't)\s+(?:(?:bao gio|duoc|nen|ever)\s+)?$/.test(prefix))continue;
  add(id,title,normalized.evidence(m.index!,m[0].length),action,severity);
 }
 const matches=input.match(/https?:\/\/[^\s<>"']+/giu)||[];
 for(const raw of [...new Set(matches)].slice(0,30))try{
  const url=new URL(raw.replace(/[),.;!?]+$/,'')),host=url.hostname.replace(/\.$/,'');
  const matchesExpected=expected?host===expected||host.endsWith('.'+expected):undefined;
  urls.push({url:url.origin,host,...(matchesExpected!==undefined?{matchesExpected}:{})});
  // Never retain a password, bearer-like query, or complete credential URL as evidence.
  if(url.username||url.password)add('url-userinfo','Đường link chứa phần đăng nhập gây nhầm tên miền',host+' (phần trước @ đã ẩn)','Đọc tên miền thực ở phần sau dấu @; không nhập thông tin xác thực.','medium');
  if(url.protocol==='http:')add('http','Liên kết không dùng HTTPS',host,'Không nhập thông tin nhạy cảm qua kết nối này. HTTPS cũng không tự chứng minh website đáng tin.');
  if(/(?:^|\.)xn--/.test(host))add('idn','Tên miền có ký tự quốc tế được mã hóa',host,'Kiểm tra với địa chỉ chính thức; ký tự quốc tế không tự chứng minh lừa đảo.');
  if(/^(?:\d{1,3}\.){3}\d{1,3}$/.test(host)||host.startsWith('['))add('ip-host','Liên kết dùng địa chỉ IP',host,'Đối chiếu nguồn gửi; địa chỉ IP không xác minh thương hiệu.');
  if(['bit.ly','tinyurl.com','t.co','shorturl.at','is.gd'].includes(host))add('short-link','Đường link rút gọn che địa chỉ đích',host,'Xin địa chỉ đầy đủ và xác minh qua kênh độc lập.');
  if(matchesExpected===false)add('domain-mismatch','Tên miền khác địa chỉ cậu chọn đối chiếu',host+' ≠ '+expected,'Dùng địa chỉ chính thức cậu tự biết. Khác tên miền có thể có lý do hợp lệ; chưa đủ kết luận giả mạo.','medium');
 }catch{/* No network requests, script execution or redirects. */}
 const priority=signals.some(s=>s.severity==='high')?'attention':signals.length?'review':'no-match';
 return {signals,urls,priority,expectedDomain:expected||null,scope:'Phân tích văn bản và cấu trúc URL tại máy; không mở trang, kiểm tra danh tiếng, tệp tải hay giao dịch. Không có dấu hiệu không đồng nghĩa an toàn.'};
}
