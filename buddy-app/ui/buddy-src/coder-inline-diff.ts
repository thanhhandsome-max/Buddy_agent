import {structuredPatch} from 'diff';

export type InlineDiffRow={kind:'context'|'added'|'removed';oldLine:number|null;newLine:number|null;text:string};
export type InlineDiffSection={kind:'fold';count:number}|{kind:'hunk';oldStart:number;newStart:number;rows:InlineDiffRow[]};

/** Build a bounded-context, line-numbered diff for the Coder review pane. */
export function coderInlineDiff(oldText:string,newText:string,context=3):{sections:InlineDiffSection[];added:number;removed:number}{
 if(oldText===newText)return {sections:[],added:0,removed:0};
 const patch=structuredPatch('before','after',oldText,newText,'','',{context});
 const sections:InlineDiffSection[]=[];let oldCursor=1,newCursor=1,added=0,removed=0;
 for(const hunk of patch.hunks){
  if(hunk.oldStart>oldCursor||hunk.newStart>newCursor){const skipped=Math.max(hunk.oldStart-oldCursor,hunk.newStart-newCursor);if(skipped>0)sections.push({kind:'fold',count:skipped});}
  let oldLine=hunk.oldStart,newLine=hunk.newStart;const rows:InlineDiffRow[]=[];
  for(const raw of hunk.lines){const marker=raw[0],text=raw.slice(1);if(marker===' '){rows.push({kind:'context',oldLine:oldLine++,newLine:newLine++,text});}else if(marker==='-'){rows.push({kind:'removed',oldLine:oldLine++,newLine:null,text});removed++;}else if(marker==='+'){rows.push({kind:'added',oldLine:null,newLine:newLine++,text});added++;}}
  sections.push({kind:'hunk',oldStart:hunk.oldStart,newStart:hunk.newStart,rows});oldCursor=oldLine;newCursor=newLine;
 }
 const lineCount=(text:string)=>text===''?0:text.split('\n').length-(text.endsWith('\n')?1:0),totalOld=lineCount(oldText),totalNew=lineCount(newText);
 const trailing=Math.max(totalOld-oldCursor+1,totalNew-newCursor+1);if(trailing>0)sections.push({kind:'fold',count:trailing});
 return {sections,added,removed};
}
