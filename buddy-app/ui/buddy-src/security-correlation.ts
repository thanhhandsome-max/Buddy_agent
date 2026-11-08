import type {SecurityFinding} from './security-analysis.ts';
function record(value: unknown): Record<string, unknown> {
 return value && typeof value==='object' && !Array.isArray(value) ? value as Record<string,unknown> : {};
}
function text(value: unknown) {
 return typeof value==='number' || typeof value==='string' ? String(value) : '';
}
/** Correlates explicit logged events; never executes commands or follows URLs. */
export function correlateSecurityEvents(lines:string[]):SecurityFinding[]{
 const findings:SecurityFinding[]=[],failures=new Map<string,{at:number;line:number}[]>();
 const add=(line:number,severity:SecurityFinding['severity'],title:string,recommendation:string)=>{if(findings.length<100)findings.push({id:'correlation-'+line+'-'+findings.length,line,severity,title,recommendation,source:'Tương quan sự kiện cục bộ',evidence:lines[line-1]?.slice(0,700)??''});};
 for(const [index,raw]of lines.entries()){
  let e:Record<string,unknown>;try{e=record(JSON.parse(raw));}catch{continue;}
  const win=record(e.win),data=record(e.EventData||win.eventdata),system=record(win.system||e.System);
  const id=String(e.EventID??e.event_id??system.eventID??system.EventID??'');
  const at=Date.parse(text(e.timestamp||e.TimeCreated||system.systemTime)),ip=text(e.src_ip||e.IpAddress||data.IpAddress||data.ipAddress),account=text(e.AccountName||e.TargetUserName||data.TargetUserName||data.targetUserName);
  if(['4625','4624'].includes(id)&&Number.isFinite(at)&&ip&&account&&ip!=='-'&&ip!=='127.0.0.1'&&ip!=='::1'){
   const key=ip+'\0'+account,prior=(failures.get(key)||[]).filter(f=>at>=f.at&&at-f.at<=300000);
   if(id==='4625'){prior.push({at,line:index+1});failures.set(key,prior);if(prior.length===5&&prior[0])add(index+1,'high',`5 lần đăng nhập thất bại cùng IP/tài khoản trong 5 phút`,`Đối chiếu IP ${ip.slice(0,80)} và tài khoản ${account.slice(0,80)}; lần đầu tại dòng ${prior[0].line}. Có thể là dò mật khẩu hoặc cấu hình sai; xác minh trước khi khóa truy cập.`);}
   else if(prior.length>=5&&prior[0]){add(index+1,'high','Đăng nhập thành công sau chuỗi thất bại cùng nguồn',`Đối chiếu dòng ${prior[0].line}–${index+1}, chủ tài khoản, thiết bị và phiên đăng nhập; đây là chuỗi cần ưu tiên điều tra, chưa xác nhận xâm nhập.`);failures.delete(key);}
  }
  if(id==='7045')add(index+1,'medium','Dịch vụ Windows mới được cài','Kiểm tra tên dịch vụ, đường dẫn binary, chữ ký và người cài. Đối chiếu thay đổi quản trị được duyệt trước khi dừng dịch vụ.');
  if(id==='4698')add(index+1,'medium','Tác vụ hẹn giờ mới được tạo','Kiểm tra tác giả, tài khoản chạy và hành động trong XML tác vụ; xác minh nhu cầu hợp lệ.');
  if(id==='4719')add(index+1,'medium','Chính sách kiểm toán Windows thay đổi','Đối chiếu tài khoản quản trị và kế hoạch thay đổi; việc giảm ghi log cần được giải thích.');
  if(id==='1116')add(index+1,'high','Microsoft Defender ghi nhận mối đe dọa','Đọc tên phát hiện và trạng thái xử lý từ Defender. Có phát hiện không đồng nghĩa mối đe dọa vẫn đang hoạt động; kiểm tra sự kiện xử lý liên quan.');
  if(id==='5007')add(index+1,'medium','Cấu hình Microsoft Defender thay đổi','Đối chiếu cấu hình trước/sau, đặc biệt exclusion và real-time protection; cập nhật hoặc quản trị hợp lệ cũng có thể tạo sự kiện này.');
  const command=String(e.CommandLine||data.CommandLine||data.commandLine||e.command_line||'');
  if(['4688','1'].includes(id)&&/\b(?:vssadmin|wbadmin|bcdedit)(?:\.exe)?\b/i.test(command)&&/delete\s+(?:shadows|catalog)|recoveryenabled\s+no|ignoreallfailures/i.test(command))add(index+1,'high','Dòng lệnh có dấu hiệu làm suy yếu phục hồi hệ thống','Xác minh tiến trình cha, người chạy và tác vụ bảo trì. Giữ log và kiểm tra bản sao ngoại tuyến; không thực thi lại dòng lệnh trong log.');
  if(['4688','1'].includes(id)&&/\b(?:powershell|pwsh)(?:\.exe)?\b/i.test(command)&&/(?:DownloadString|Invoke-WebRequest|iwr)\b/i.test(command)&&/(?:Invoke-Expression|\biex\b)/i.test(command))add(index+1,'high','Tiến trình PowerShell có mẫu tải và thực thi nội dung','Kiểm tra URL dưới dạng dữ liệu, tiến trình cha, chữ ký và nội dung script từ nguồn thu thập tin cậy. Không mở URL hoặc chạy script để thử.');
 }
 return findings;
}
