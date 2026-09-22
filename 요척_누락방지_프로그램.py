import tkinter as tk
from tkinter import ttk, messagebox
CATEGORIES=[("겉감",["앞판","뒤판","소매","칼라/후드","덧장/플랩"]),("안감",["몸판안감","포켓안감"]),("심지",["몸판심지","기타심지"]),("오비심지",["앞오비심지","뒤오비심지"]),("배색",["배색"]),("소매안감",["소매안감"]),("포켓",["앞주머니","뒤주머니"]),("오비",["앞오비","뒤오비"]),("뎅고",["뎅고"]),("부속",["테이프/고무/끈","기타부속"])]
class App:
 def __init__(self,r):
  self.r=r;r.title("요척 누락 방지 관리 프로그램");r.geometry("1050x700");top=ttk.Frame(r,padding=10);top.pack(fill="x");self.entries={}
  for i,n in enumerate(["스타일명","품번","원단","작업자"]):
   ttk.Label(top,text=n).grid(row=0,column=i*2);e=ttk.Entry(top,width=20);e.grid(row=0,column=i*2+1,padx=(5,15));self.entries[n]=e
  fr=ttk.Frame(r,padding=10);fr.pack(fill="both",expand=True);cols=("구분","구성품","패턴 확인","요척 입력","패턴 개수","비고");self.t=ttk.Treeview(fr,columns=cols,show="headings")
  for c,w in zip(cols,[100,180,100,100,100,300]):self.t.heading(c,text=c);self.t.column(c,width=w,anchor="center" if c!="비고" else "w")
  sb=ttk.Scrollbar(fr,orient="vertical",command=self.t.yview);self.t.configure(yscrollcommand=sb.set);self.t.pack(side="left",fill="both",expand=True);sb.pack(side="right",fill="y");self.data={}
  for cat,items in CATEGORIES:
   for item in items:iid=self.t.insert("","end",values=(cat,item,"□","□","",""));self.data[iid]=[cat,item,False,False,0,""]
  self.t.bind("<Double-1>",self.edit);b=ttk.Frame(r,padding=10);b.pack(fill="x")
  ttk.Button(b,text="합계 보기",command=self.total).pack(side="left",padx=4);ttk.Button(b,text="선택 항목 수정",command=self.edit).pack(side="left",padx=4);ttk.Button(b,text="초기화",command=self.reset).pack(side="left",padx=4)
 def edit(self,e=None):
  s=self.t.selection()
  if not s:return
  iid=s[0];d=self.data[iid];w=tk.Toplevel(self.r);w.title(f"{d[0]} / {d[1]}");w.grab_set();f=ttk.Frame(w,padding=18);f.pack();a=tk.BooleanVar(value=d[2]);q=tk.BooleanVar(value=d[3]);n=tk.IntVar(value=d[4])
  ttk.Label(f,text=f"{d[0]} / {d[1]}",font=("",12,"bold")).pack(pady=8);ttk.Checkbutton(f,text="패턴 확인",variable=a).pack(anchor="w");ttk.Checkbutton(f,text="요척 입력 확인",variable=q).pack(anchor="w");row=ttk.Frame(f);row.pack(pady=8);ttk.Label(row,text="패턴 개수").pack(side="left");tk.Spinbox(row,from_=0,to=999,textvariable=n,width=7).pack(side="left",padx=10);ttk.Label(f,text="비고").pack(anchor="w");note=tk.Text(f,width=40,height=4);note.insert("1.0",d[5]);note.pack()
  def save():
   d[2]=a.get();d[3]=q.get();d[4]=n.get();d[5]=note.get("1.0","end-1c");self.t.item(iid,values=(d[0],d[1],"✓" if d[2] else "□","✓" if d[3] else "□",d[4] or "",d[5]));w.destroy()
  ttk.Button(f,text="저장",command=save).pack(fill="x",pady=10)
 def total(self):
  sums={c:0 for c,_ in CATEGORIES}
  for d in self.data.values():sums[d[0]]+=d[4]
  w=tk.Toplevel(self.r);w.title("항목별 총 패턴 개수");w.geometry("400x500");t=ttk.Treeview(w,columns=("항목","합계"),show="headings");t.heading("항목",text="항목");t.heading("합계",text="총 패턴 개수");t.column("항목",width=180);t.column("합계",width=150,anchor="center");t.pack(fill="both",expand=True,padx=15,pady=15)
  for c,_ in CATEGORIES:t.insert("","end",values=(c,sums[c]))
 def reset(self):
  if not messagebox.askyesno("초기화","입력한 내용을 모두 초기화할까요?"):return
  for e in self.entries.values():e.delete(0,"end")
  for iid,d in self.data.items():d[2:]=[False,False,0,""];self.t.item(iid,values=(d[0],d[1],"□","□","",""))
if __name__=="__main__":
 r=tk.Tk()
 try:ttk.Style().theme_use("vista")
 except:pass
 App(r);r.mainloop()
