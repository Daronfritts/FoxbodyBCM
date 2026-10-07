#!/usr/bin/env python3
"""Regenerate the terminal-to-terminal SVG documentation; no runtime wiring changes."""
from pathlib import Path
from html import escape as esc
import textwrap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/schematics'
C = {'power':'#c62828','switched':'#d66700','ground':'#202020','signal':'#1565c0','motor':'#26803c','analog':'#7b3294','bus':'#616161'}
INPUTS = ['Driver door ajar','Passenger door ajar','Hatch ajar','Hood open','Brake state (interface)','Clutch pedal','Parking brake','Reverse state (interface)','Start / defrost button','Defrost intent / separate contact','Glove-box hatch button','Lock command','Unlock command','Driver window UP','Driver window DOWN','Passenger window UP','Passenger window DOWN','Wiper mist','Wiper intermittent','Wiper low','Wiper high','Washer request','Headlight request','High beam request','Left turn request','Right turn request','Hazard request','RUN sense (interface)','Wiper park (interface)','Fuel-door request','Spare','Spare']
OUTPUTS = ['Park / marker','Puddle LEDs','Courtesy LEDs','Left turn','Right turn','Horn relay coil','Spare (defrost moved to RLY-04)','Hatch release','Fuel-door release','Low-beam relay coil','High-beam relay coil','Wiper LOW control','Wiper HIGH control','Washer pump / relay','Spare (START moved to RLY-03)','Spare']

class Sheet:
 def __init__(self,name,title,sub):
  self.name=name; self.y=190; self.parts=[]
  self.text(40,48,'FOXBODY BCM / '+title,30,True)
  self.text(40,82,sub,17)
  self.text(40,113,'DESIGN DRAFT • TBD = terminal/pin or wire specification not yet verified • Repeated device labels refer to the same device.',16)
  self.text(40,145,'Wire colors indicate function. Actual harness colors and AWG remain TBD unless explicitly printed.',16)
 def text(self,x,y,s,size=17,bold=False,anchor='start',color='#111'):
  self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{anchor}" fill="{color}">{esc(s)}</text>')
 def rect(self,x,y,w,h): self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white" stroke="#222" stroke-width="2.5"/>')
 def wire(self,points,kind='signal',label=None):
  self.parts.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in points)}" fill="none" stroke="white" stroke-width="9"/>')
  self.parts.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in points)}" fill="none" stroke="{C[kind]}" stroke-width="3"/>')
  for x,y in (points[0],points[-1]): self.parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="white" stroke="{C[kind]}" stroke-width="2"/>')
 def bundle(self,title,left,right,rows,note=''):
  """Every row is a conductor between two explicitly labelled device terminals."""
  y=self.y; self.text(40,y,title,21,True); top=y+24; h=76+len(rows)*44
  self.rect(60,top,420,h); self.rect(1320,top,420,h)
  for x,name in [(270,left),(1530,right)]:
   for i,line in enumerate(textwrap.wrap(name,34)):
    self.text(x,top+28+i*22,line,18,True,'middle')
  for i,(a,b,label,kind) in enumerate(rows):
   yy=top+83+i*44
   self.text(460,yy-8,a,16,False,'end'); self.text(1340,yy-8,b,16)
   if kind == 'unused':
    self.text(900,yy-10,'UNASSIGNED • LEAVE UNWIRED',16,False,'middle','#616161')
   else:
    self.wire([(480,yy),(1320,yy)],kind)
    self.text(900,yy-10,label,16,False,'middle',C[kind])
  self.y=top+h+30
  if note:
   for line in textwrap.wrap(note,165): self.text(60,self.y,line,16); self.y+=23
  self.y+=28
 def notes(self,lines):
  self.text(40,self.y,'CIRCUIT NOTES',20,True); self.y+=30
  for s in lines:
   for line in textwrap.wrap(s,165): self.text(60,self.y,line,16); self.y+=23
  self.y+=30
 def save(self):
  self.y+=25
  for i,(k,v) in enumerate(C.items()):
   x=40+i*245; self.wire([(x,self.y),(x+35,self.y)],k); self.text(x+45,self.y+5,k,15)
  self.text(40,self.y+38,'Source: repository design docs, fuse schedule and hardware inventory. Pin order is not a physical PCB layout.',15)
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="{self.y+70}" viewBox="0 0 1800 {self.y+70}" role="img"><title>{esc(self.name)}</title><desc>Labelled rectangular devices, terminal names at every conductor end, and continuous wire paths. Design draft.</desc><g font-family="DejaVu Sans,Arial,sans-serif">'+''.join(self.parts)+'</g></svg>\n'
  (OUT/self.name).write_text(svg)

def row(a,b,label='',kind='signal'): return (a,b,label,kind)
def power(s,title,fuse,amp,device,terminal='VIN (verify)'):
 s.bundle(title,'BCM fused distribution',device,[row(f'{fuse} OUT',terminal,f'{fuse} {amp}A • +12V','power'),row('CHASSIS GND','GND (verify)','Ground return','ground')],f'{fuse} fuse sits upstream of this conductor; gauge/color TBD. Verify device terminal order.')
def switches(s,title,labels):
 s.bundle(title,'Intercepted switches / interface','Input Board IN-01 (24DIB32)',[row('Contact / sink (pin TBD)' if i < 30 else 'No connection',f'X{i:02}',label,'signal' if i < 30 else 'unused') for i,label in labels]+[row('Switch common (pin TBD)','GND / input return (verify)','Low-current ground-switch return','ground')],'Factory +12V sources use a protected sinking interface. X labels are input channel numbers, not factory connector pin numbers.')
def relay(s,title,fuse,amp,control,term,load):
 y=s.y; s.text(40,y,title,22,True)
 s.rect(60,y+35,420,125); s.text(270,y+67,'FUSED DISTRIBUTION',19,True,'middle')
 s.text(460,y+122,f'{fuse} OUT',17,False,'end')
 s.rect(740,y+35,320,280); s.text(900,y+68,title,18,True,'middle')
 s.rect(1320,y+35,420,280); s.text(1530,y+68,load,18,True,'middle')
 s.text(760,y+122,'30',25,True); s.text(1040,y+122,'87',25,True,'end')
 s.wire([(480,y+130),(740,y+130)],'power'); s.text(610,y+118,f'{fuse} {amp}A',17,True,'middle')
 s.wire([(1060,y+130),(1320,y+130)],'switched'); s.text(1190,y+118,'Load +12V',17,False,'middle')
 s.text(1340,y+122,'+ / factory pin TBD',16)
 s.rect(60,y+190,420,125); s.text(270,y+222,control,18,True,'middle'); s.text(460,y+267,term,18,True,'end')
 s.text(760,y+267,'86',25,True); s.wire([(480,y+275),(740,y+275)],'switched'); s.text(610,y+263,'Coil +12V',17,False,'middle')
 s.text(900,y+300,'85',25,True,'middle'); s.wire([(900,y+315),(900,y+365)],'ground'); s.text(900,y+390,'CHASSIS GND',17,True,'middle')
 s.text(1530,y+300,'− / ground pin TBD',16,False,'middle'); s.wire([(1530,y+315),(1530,y+365)],'ground'); s.text(1530,y+390,'CHASSIS GND',17,True,'middle')
 s.text(60,y+425,'87a unused / insulated. Suppress coil; 86 positive / 85 ground. Vehicle current flows through 30–87 only.',16)
 s.y=y+480

def direct(s,title,fuse,amp,yout,load):
 y=s.y; s.text(40,y,title.upper()+' / POWER AND LOAD',22,True)
 for x,label in [(60,'FUSED DISTRIBUTION'),(740,'Output Board OUT-01'),(1320,load)]:
  s.rect(x,y+35,420 if x!=740 else 320,180); s.text(x+(210 if x!=740 else 160),y+68,label,18,True,'middle')
 s.text(460,y+122,f'{fuse} OUT',16,False,'end'); s.text(760,y+122,'Load supply TBD',16)
 s.wire([(480,y+130),(740,y+130)],'power'); s.text(610,y+118,f'{fuse} {amp}A',17,True,'middle')
 s.text(1040,y+122,yout,18,True,'end'); s.text(1340,y+122,'+ / pin TBD',16)
 s.wire([(1060,y+130),(1320,y+130)],'switched'); s.text(1190,y+118,'Switched +12V',16,False,'middle')
 s.text(900,y+202,'GND (verify)',16,False,'middle'); s.wire([(900,y+215),(900,y+260)],'ground'); s.text(900,y+283,'BOARD GND',16,False,'middle')
 s.text(1530,y+202,'− / pin TBD',16,False,'middle'); s.wire([(1530,y+215),(1530,y+260)],'ground'); s.text(1530,y+283,'CHASSIS GND',16,False,'middle')
 s.text(60,y+322,'Direct only if ≤4A continuous and inrush/thermal limits verified; otherwise add a dedicated relay/driver.',16)
 s.text(60,y+349,'Feed-bank terminal allocation, wire gauge/color and load pins TBD; fuse must protect the final wire.',16)
 s.y=y+400

s=Sheet('01_core_power.svg','CORE POWER / GROUND','Battery and distribution wiring; fan feeds and starter main cable remain outside the BCM main fuse.')
s.bundle('Main feed','Battery','BCM distribution / F00',[row('+','F00 IN','Battery cable • protection near source','power'),row('-','CHASSIS / ENGINE BOND','Heavy ground bond','ground')])
s.bundle('Main protection','F00 main fuse • 125A baseline','BCM distribution block',[row('OUT','+12V BUS','F00 125A protected feed','power')])
for f,a,d in [('F01',5,'5V Power Supply'),('F02',3,'Input Board IN-01'),('F03',5,'Output Board OUT-01'),('F04',40,'Window Driver DRV-02'),('F05',20,'Lock Driver'),('F23',5,'Sensor regulator / analog supply')]: power(s,'Branch '+f,f,a,d)
s.bundle('Regulated controller supply','5V Power Supply','BCM Controller / Raspberry Pi 4B',[row('5V +','5V power input (connector TBD)','Regulated 5V • never raw +12V','power'),row('5V -','Power GND','Electronics return','ground')])
s.bundle('Ground architecture','Battery negative / chassis bond','Ground distribution',[row('BODY BOND','HEAVY GND BUS','Motors / relays / loads','ground'),row('BODY BOND','ELECTRONICS GND BUS','Pi / I/O / sensors','ground')])
s.notes(['F00 = 125A per current fuse schedule; this replaces the stale 80A value in the schematic specification. Fuse/wire sizing remains a design baseline.','Cooling F21/F22 are independent battery feeds. Starter main battery cable is separate; F18 protects only the starter-control branch.','High-current grounds do not flow through Pi/sensor wiring. Transient protection and the 5V connector/cable must be finalized.']); s.save()

s=Sheet('02_input_board.svg','INPUT BOARD','Every X00–X31 channel is shown with its incoming conductor.')
s.bundle('Board supply / commons','F02 fused +12V / ground bus','Input Board IN-01',[row('F02 OUT','VIN (verify)','F02 3A board power','power')]+[row('F02 OUT',f'COM{i} (verify)','NPN bank common +12V (verify)','power') for i in range(4)]+[row('GND','GND (verify)','Board power return','ground')],'Verify the COM bank polarity and numbering against the exact board before connecting.')
for start in (0,8,16,24): switches(s,f'Input channels X{start:02}–X{start+7:02}',list(enumerate(INPUTS[start:start+8],start)))
s.bundle('RS485 conductors','Input Board IN-01','Isolated USB-RS485 Adapter',[row('A+ (verify)','A / D+ (verify)','RS485 twisted pair A','bus'),row('B- (verify)','B / D- (verify)','RS485 twisted pair B','bus')],'Isolated adapter bus-reference/shield connection follows its specific manual; do not bridge isolation by guessing a ground connection.')
s.bundle('Protected +12V input example','Factory brake / reverse / RUN','Protected input interface (TBD)',[row('Signal +12V (pin TBD)','12V IN','Factory signal • never direct to Pi','signal'),row('Factory GND','GND / return (TBD)','Interface return','ground')])
s.bundle('Conditioned input example','Protected input interface (TBD)','Input Board IN-01',[row('SINK OUT','X04 / X07 / X27','Choose the matching assigned channel','signal')])
s.notes(['The repurposed defrost/start button uses X08. X09 is a separate contact/input only if physically present; software intent handling does not create a second wire.','X30/X31 are unassigned: shown in the map, leave unwired. Verify ground-switch behavior on every factory switch. Preserve independent brake-light operation.']); s.save()

s=Sheet('03_output_board.svg','OUTPUT / RELAY BOARD','Mechanical relay contacts command Bosch coils; MOSFET board controls the remaining planned loads.')
power(s,'Output-board electronics','F03',5,'Output Board OUT-01')
s.bundle('Low-voltage logic / protected level interface','BCM / I/O Expander','3.3V-compatible sink interface (TBD)',[row(f'GPIO for CH{i} (pin TBD)',f'LOGIC IN {i} (TBD)',f'Channel {i} logic command','signal') for i in range(1,17)]+[row('Logic GND','LOGIC GND','Logic reference','ground')],'Assign exact GPIO/interface terminals before installation; each line is a separate conductor.')
s.bundle('12V output-board control','Sink interface / control supply','Output Board OUT-01',[row(f'Sink OUT {i} (TBD)',f'X{i} (verify)',f'Channel {i} isolated input control','signal') for i in range(1,17)]+[row('Control common (TBD)','COM (verify)','8–25V input circuit • polarity TBD','power')],'Do not wire Pi GPIO directly to the OPMSD16 12V input version. Exact sinking/common circuit is still unresolved.')
for start in (0,8):
 s.bundle(f'MOSFET outputs Y{start+1:02}–Y{start+8:02}','Output Board OUT-01','Assigned downstream circuits',[row(f'Y{i+1:02}','Load / coil pin (TBD)' if i not in (6,14,15) else 'No connection',OUTPUTS[i],'switched' if i not in (6,14,15) else 'unused') for i in range(start,start+8)],'Map preserves existing schematic channel allocation, except Y07/Y15 are now spare after the mechanical-relay assignments. The I/O assignment plan now matches this baseline; verify against final software/HAL before installation.')
s.bundle('Mechanical relay contact wiring','Fused coil-control +12V (branch TBD)','8-channel Mechanical Relay Board',[row('+12V',f'COM{i}',f'Fused coil-control feed {i}','power') for i in range(1,5)]+[row('GND','Board GND (verify)','Relay-board supply return','ground'),row('Supply (TBD)','VCC / JD-VCC (verify)','Board supply • verify jumper arrangement','power')])
s.bundle('Mechanical relay outputs','8-channel Mechanical Relay Board','Bosch relay coils',[row('NO1','ACC 86','RLY-01 = ACC','switched'),row('NO2','RUN 86','RLY-02 = RUN / IGN','switched'),row('NO3','START 86','RLY-03 = START','switched'),row('NO4','DEFROST 86','RLY-04 = rear defrost','switched')],'NC contacts unused. Outputs 5–8 spare. Physical board RLY-01 is not the same naming scope as channel RLY-01.')
s.bundle('Mechanical relay-board logic','BCM Controller / logic interface','8-channel Mechanical Relay Board',[row(f'{name} GPIO (pin TBD)',f'IN{i} (verify)',f'{name} logic command','signal') for i,name in enumerate(['ACC','RUN','START','DEFROST'],1)]+[row('Logic GND','Logic GND (verify)','Reference if non-isolated interface','ground')],'Verify 3.3V trigger compatibility and polarity; fit a suitable interface if required. The board contacts switch +12V to Bosch coils, not vehicle load current.')
s.notes(['Remaining Y outputs and the 16-channel control interface are provisional. Software/HAL map must match the final physical terminals.','Direct MOSFET ceiling ≤4A continuous only after thermal/inrush verification. Every downstream load/coil needs its proper ground return.']); s.save()

for windows in (False,True):
 n='05_windows_hbridge.svg' if windows else '04_door_locks_hbridge.svg'; name='WINDOW DRIVER' if windows else 'LOCK DRIVER'
 s=Sheet(n,name+' / H-BRIDGE','Two motor wires per channel; neither motor conductor is permanently chassis-grounded.')
 power(s,'Driver supply','F04' if windows else 'F05',40 if windows else 20,'Window Driver DRV-02' if windows else 'Lock Driver')
 for ch,side in [(1,'DRIVER'),(2,'PASSENGER')]:
  s.bundle(side+' motor pair',name,side+(' WINDOW MOTOR' if windows else ' LOCK ACTUATOR'),[row(f'CH{ch} MOTOR A (TBD)','Motor wire 1 (pin TBD)','Reversing motor conductor 1','motor'),row(f'CH{ch} MOTOR B (TBD)','Motor wire 2 (pin TBD)','Reversing motor conductor 2','motor')],'Output labels are functional until silk-screen pinout is verified; both wires go to the H-bridge, not chassis.')
  terms=['DIR A','DIR B','PWM'] if windows else ['IN-A','IN-B']
  s.bundle(side+' logic wiring','BCM / MOTOR LOGIC (GPIO TBD)',name,[row(f'{side} {t} (pin TBD)',f'CH{ch} {t} (TBD)','3.3V-compatible control • verify','signal') for t in terms]+[row('LOGIC GND','SIGNAL GND (TBD)','Control reference','ground')])
 switches(s,'Switch commands',[(i,INPUTS[i]) for i in (range(13,17) if windows else range(11,13))])
 if windows:
  s.bundle('Current-sensor outputs','Window Hall sensors','Protected Analog Board',[row('Driver VOUT','DR_WIN_CURRENT (ADC TBD)','Driver current signal','analog'),row('Passenger VOUT','PS_WIN_CURRENT (ADC TBD)','Passenger current signal','analog'),row('Sensor GND','SENSOR GND','Electronics return','ground')],'Route each measured power conductor through its Hall sensor; final sensor type, power terminals and supply voltage TBD.')
 s.notes(['Selected hardware is the dual H-bridge from the current inventory, not the superseded Cytron part names in older docs.','Window module: 9–30V supply, A/B plus PA/PB PWM; exact channel pin names/order TBD. Reversal dead-time, timeout and current shutdown are required.' if windows else 'Lock module: 3–14V supply, 2.2–6V logic, 5A continuous/9A peak per channel. Verify compatibility with charging-system voltage and transients before vehicle use. Use timed lock pulses.']); s.save()

s=Sheet('06_lighting_horn_defrost.svg','LIGHTING / HORN / DEFROST','Bosch terminal numbers at every relay connection; defrost uses mechanical relay output 4.')
for args in [('LOW-BEAM RELAY','F06',20,'Output Board OUT-01','Y10','LH / RH low-beam lamps'),('HIGH-BEAM RELAY','F07',20,'Output Board OUT-01','Y11','LH / RH high-beam lamps'),('HORN RELAY','F10',20,'Output Board OUT-01','Y06','Horn'),('REAR-DEFROST RELAY','F11',30,'Mechanical Relay Board','NO4','Rear-window grid')]: relay(s,*args)
for args in [('Park / marker','F08',15,'Y01','Park / marker lamps'),('Left turn','F09',15,'Y04','Left turn lamps'),('Right turn','F09',15,'Y05','Right turn lamps'),('Puddle','F12',5,'Y02','Puddle LEDs'),('Courtesy','F13',10,'Y03','Interior / courtesy LEDs')]: direct(s,*args)
s.bundle('Rear-defrost coil-control source','Fused +12V coil supply (TBD)','Mechanical Relay Board',[row('+12V','COM4','Coil-only feed; NC4 unused','power')])
switches(s,'Lighting commands',[(i,INPUTS[i]) for i in range(22,27)])
s.notes(['F09 is shared by left/right turn branches, not two separate added fuses. Feed bank arrangement and lamp currents remain TBD.','Start/defrost intent comes from X08, or X09 only if a separate verified contact exists. Rear grid current passes through F11 and Bosch 30/87, never the board relay contacts.','Brake lamps remain independent of BCM. Verify factory rear brake/turn arrangement and interception before installing these provisional turn outputs.','Courtesy dimming requires a PWM-capable verified power stage. Relay coils need correctly oriented suppression (86 positive, 85 ground where diode suppressed).']); s.save()

s=Sheet('07_wipers_washer_hatch.svg','WIPERS / WASHER / RELEASES','Wiper controller topology stays provisional until the Ford park circuit is verified.')
power(s,'Wiper motor power','F14',25,'Wiper power stage (TBD)')
s.bundle('Wiper control conductors','Output Board OUT-01','Wiper power stage (TBD)',[row('Y12','LOW command (TBD)','Low-speed command','switched'),row('Y13','HIGH command (TBD)','High-speed command','switched')],'Final relay/driver topology must preserve park operation and prevent simultaneous low/high commands. Do not guess Ford motor pins.')
s.bundle('Wiper motor harness','Wiper power stage (TBD)','Factory wiper motor',[row('LOW OUT (TBD)','LOW (pin TBD)','Low-speed motor conductor','motor'),row('HIGH OUT (TBD)','HIGH (pin TBD)','High-speed motor conductor','motor'),row('PARK supply (TBD)','PARK feed (pin TBD)','Park supply • exact circuit TBD','power'),row('HEAVY GND','GND (pin TBD)','Motor return','ground')])
s.bundle('Wiper park feedback','Factory wiper motor','Protected park interface (TBD)',[row('PARK sense (pin TBD)','IN (TBD)','Verify contact polarity / voltage','signal')])
s.bundle('Conditioned park feedback','Protected park interface (TBD)','Input Board IN-01',[row('SINK OUT','X28','Wiper park input','signal')])
for args in [('Washer','F15',10,'Y14','Washer pump'),('Hatch','F16',15,'Y08','Hatch-release solenoid'),('Fuel door','F17',10,'Y09','Fuel-door actuator')]: direct(s,*args)
switches(s,'Driver commands',[(i,INPUTS[i]) for i in [17,18,19,20,21,10,29]])
s.notes(['Motor/solenoid inrush and flyback may require dedicated relays/drivers even below the nominal 4A direct limit. Exact downstream terminals remain TBD.','Washer behavior is software controlled; see feature specification for passes, delay and courtesy wipe. Final park wiring needs the 1988 EVTM/verified motor harness.']); s.save()

s=Sheet('08_start_ignition_accessory.svg','PUSH START / ACC / RUN / START','Reference-style layout: mechanical board NO outputs → Bosch 86; 85 → ground; fused feed → 30; 87 → vehicle.')
# Three actual relay boxes, with separate feed / coil / load paths, matching the user's sketch.
y=s.y
s.text(40,y,'IGNITION RELAY WIRING',22,True)
s.rect(60,y+35,380,110); s.text(250,y+70,'Factory ignition feed',20,True,'middle'); s.text(250,y+105,'Yellow +12V • fused branches below',16,False,'middle'); s.text(420,y+134,'B+ (pin TBD)',16,False,'end')
s.rect(660,y+35,1080,150); s.text(1200,y+70,'8-channel Mechanical Relay Board',22,True,'middle'); s.text(1200,y+103,'COM1 / COM2 / COM3 ← fused +12V coil feed (branch TBD)',17,False,'middle'); s.text(1200,y+135,'NC contacts unused • GPIO/trigger polarity TBD',16,False,'middle')
for i,(name,fuse,amp,wire) in enumerate([('ACC','F20',30,'Factory ACC pin/color TBD'),('RUN / IGN','F19',30,'Factory RUN pins/colors TBD'),('START','F18',15,'Factory START pin/color TBD')]):
 x=100+i*570; top=y+385
 # staggered independent power feeds, no implied connected crossings
 feed_y=y+230+i*38
 s.wire([(440,y+132),(490,y+132),(490,feed_y),(x+65,feed_y),(x+65,top)],'power')
 fuse_x=(490+x+65)/2
 s.rect(fuse_x-55,feed_y-14,110,28); s.text(fuse_x,feed_y+6,f'{fuse} {amp}A',16,True,'middle')
 s.rect(x,top,320,170); s.text(x+160,top+34,name+' BOSCH',20,True,'middle')
 s.text(x+65,top+63,'30',25,True,'middle'); s.text(x+260,top+63,'86',25,True,'middle')
 s.text(x+65,top+141,'87',25,True,'middle'); s.text(x+260,top+141,'85',25,True,'middle')
 no_x=680+i*430; s.text(no_x,y+175,f'NO{i+1} = {name}',17,True,'middle')
 # coil route vertical down to right of each relay, then in from right at 86
 lane=x+370
 s.wire([(no_x,y+185),(no_x,y+330),(lane,y+330),(lane,top+60),(x+320,top+60)],'switched')
 s.wire([(x+320,top+138),(lane,top+138),(lane,top+205)],'ground')
 s.text(lane,top+228,'CHASSIS GND',15,False,'middle')
 s.rect(x,top+260,400,100); s.text(x+200,top+293,name+' vehicle circuit',19,True,'middle'); s.text(x+200,top+322,wire,16,False,'middle'); s.text(x+65,top+350,'IN (pin TBD)',16)
 s.wire([(x+65,top+170),(x+65,top+260)],'switched')
 s.text(x+160,top+192,'87a unused / insulated',15,False,'middle')
# Solid dots on the common feed identify intentional branch junctions.
for yy in (y+230,y+268):
 s.parts.append(f'<circle cx="490" cy="{yy}" r="5" fill="{C["power"]}"/>')
s.y=y+805
s.bundle('Coil feed wiring','Fused coil-control supply (TBD)','Mechanical Relay Board',[row('+12V','COM1','ACC contact common','power'),row('+12V','COM2','RUN contact common','power'),row('+12V','COM3','START contact common','power')],'Fuse/gauge for the separate low-current coil feed must be finalized. Vehicle branch fuses protect Bosch 30/87 paths; do not carry vehicle loads through board contacts.')
switches(s,'Momentary defrost/start button and interlocks',[(8,INPUTS[8]),(5,INPUTS[5]),(4,INPUTS[4]),(27,INPUTS[27])])
s.bundle('Button ground contact','Momentary start / defrost button','Chassis ground',[row('Common contact (pin TBD)','GND','Other switch contact goes to X08','ground')])
s.bundle('Starter control destination','Factory START circuit','Starter solenoid control',[row('START out (pin TBD)','S (via verified factory interlock)','Control only • not starter motor cable','switched')])
s.notes(['RLY-01 = ACC; RLY-02 = RUN; RLY-03 = START. Bosch coil terminals: 86 positive, 85 ground. Use suppressed automotive relays with correct polarity.','The reference sketch shows candidate factory wire colors. Only yellow battery feed is identified here; confirm ACC/RUN/START colors and connector pins from the actual harness/EVTM before terminating.','Crossing lines have no electrical connection. Every feed starts at the same explicitly labelled factory B+ terminal; each Bosch 30 branch has its labelled fuse.','Retain verified clutch/RPM crank interlocks and fail-off starter command. RUN must remain active during crank. Software button/ACC/override behavior is defined separately in docs/20_feature_specification.md.']); s.save()

s=Sheet('09_cooling_fans.svg','COOLING FANS','Independent battery feeds; exact Focus fan relay/PWM controller has not been frozen.')
for i in (1,2):
 f='F21' if i==1 else 'F22'
 s.bundle(f'Fan {i} battery protection','Battery + / heavy chassis','Fan '+str(i)+' fuse / ground',[row('+',f'{f} IN',f'{f} 50A baseline • separate battery feed','power'),row('CHASSIS GND','HEAVY GND','High-current return','ground')])
 s.bundle(f'Fan {i} monitored power conductor',f'{f} 50A fuse',f'Fan {i} Hall current sensor (TBD)',[row('OUT','CURRENT PATH IN','Protected high-current conductor','power')],'Pass-through Hall aperture or series sensor terminals depend on selected hardware; do not substitute a small signal terminal.')
 s.bundle(f'Fan {i} power stage',f'Fan {i} Hall sensor / ground',f'Fan {i} controller (TBD)',[row('CURRENT PATH OUT','B+ (pin TBD)','High-current supply','power'),row('HEAVY GND','GND (pin TBD)','Power-stage ground','ground')])
 s.bundle(f'Fan {i} motor connections',f'Fan {i} controller (TBD)',f'Fan {i} motor',[row('MOTOR OUT (TBD)','+ (pin TBD)','Controlled motor feed','motor'),row('RETURN (TBD)','- (pin TBD)','Motor return • topology TBD','ground')],'These are functional terminals, not a Focus connector pinout. Do not install until controller type and pinout are confirmed.')
 s.bundle(f'Fan {i} current feedback',f'Fan {i} Hall sensor (TBD)','Protected Analog Board',[row('VOUT','FAN_CURRENT '+str(i)+' (ADC TBD)','Current sense','analog'),row('Sensor GND','SENSOR GND','Electronics return','ground')])
s.bundle('Normal / backup control inputs','BCM / MicroSquirt','Fail-safe arbitration interface (TBD)',[row('FAN command (pin TBD)','BCM IN (TBD)','Normal fan request','signal'),row('Backup FAN output (TBD)','ECU IN (TBD)','ECU emergency request','signal')],'Do not tie BCM outputs to ECU outputs directly. Exact relay/PWM authority and electrical interface remain TBD.')
s.bundle('Fan commands','Fail-safe arbitration interface (TBD)','Fan controllers (TBD)',[row('FAN1 OUT (TBD)','Fan 1 CONTROL (TBD)','Relay enable or PWM • unresolved','signal'),row('FAN2 OUT (TBD)','Fan 2 CONTROL (TBD)','Relay enable or PWM • unresolved','signal')])
s.notes(['Fans stay outside F00. Measure inrush and select proper wiring/protection for the exact motor/controller.','Use engine coolant data for normal control, up to 3-minute after-run, overheat command and current diagnostics per feature specification. Hall sensor supply voltage/pins still TBD.']); s.save()

s=Sheet('10_sensors_analog_comms.svg','SENSORS / ANALOG / COMMUNICATIONS','Protected sensing and bus conductors; unresolved hardware uses functional terminal labels followed by TBD.')
power(s,'Sensor supply','F23',5,'Sensor voltage regulator')
s.bundle('Regulated sensor rails','Sensor voltage regulator','Analog Board / sensor supply',[row('3.3V / 5V (TBD)','VCC (voltage TBD)','Select rated rail for each device','power'),row('GND','SENSOR GND','Electronics reference','ground')])
s.bundle('Fuel sender wiring','Factory fuel sender','Protected excitation / ADC front-end',[row('Sender (pin TBD)','SENDER IN (TBD)','Resistive fuel-level circuit','analog'),row('Sender ground (pin TBD)','SENSOR RETURN (TBD)','Verify factory sender ground','ground')])
s.bundle('Fuel measurement','Protected fuel front-end','Analog Board (ADC TBD)',[row('SCALED OUT','FUEL LEVEL (channel TBD)','Protected fuel signal','analog')])
s.bundle('Other analog measurements','Sensors / protected front-ends','Analog Board (ADC TBD)',[row('Battery current VOUT','BAT_CURRENT (channel TBD)','Battery current','analog'),row('Driver window VOUT','DR_WIN_CURRENT (channel TBD)','Driver window current','analog'),row('Passenger window VOUT','PS_WIN_CURRENT (channel TBD)','Passenger window current','analog'),row('Fan 1 VOUT','FAN1_CURRENT (channel TBD)','Fan 1 current','analog'),row('Fan 2 VOUT','FAN2_CURRENT (channel TBD)','Fan 2 current','analog'),row('Scaled battery voltage','BAT_VOLTAGE (channel TBD)','Protected voltage divider','analog'),row('Pressure VOUT (optional)','SPARE (channel TBD)','Pressure transducer if BCM-owned','analog'),row('Sensor GND','SENSOR GND','Sensor electronics returns','ground')],'A0–A7 in older drawings were conceptual; actual ADC hardware and physical channels remain unassigned.')
s.bundle('Digital sensor / expander bus','BCM Controller / Raspberry Pi','I2C sensors / MCP23017 (verify)',[row('GPIO2 / physical 3','SDA','I2C data • 3.3V logic','bus'),row('GPIO3 / physical 5','SCL','I2C clock • 3.3V logic','bus'),row('GND (pin TBD)','GND','Bus reference','ground'),row('Regulated rail (TBD)','VCC (voltage TBD)','Verify module rail / pull-up voltage','power')],'Includes ambient light, cabin humidity/temp and IMU if I2C versions selected. Assign unique addresses. Sensors must not pull Pi bus lines up to 5V.')
s.bundle('1-Wire temperature sensors','BCM / protected 1-Wire interface','Ambient / enclosure sensors',[row('DATA (GPIO TBD)','DQ (pin TBD)','1-Wire data • pull-up TBD','bus'),row('Rated rail (TBD)','VDD (pin TBD)','Sensor supply','power'),row('Sensor GND','GND (pin TBD)','Sensor reference','ground')])
s.bundle('RS485 bus','Input Board IN-01','Isolated USB-RS485 Adapter',[row('A+ (verify)','A / D+ (verify)','Twisted pair A','bus'),row('B- (verify)','B / D- (verify)','Twisted pair B','bus')])
s.bundle('USB connection','Isolated USB-RS485 Adapter','BCM Controller',[row('USB connector','USB host','Standard USB cable • not discrete GPIO','bus')])
s.bundle('ECU serial connection','MicroSquirt serial connector','Compatible serial / USB interface',[row('TX (pin TBD)','RX (pin TBD)','ECU-to-host serial','bus'),row('RX (pin TBD)','TX (pin TBD)','Host-to-ECU serial','bus'),row('Serial GND (pin TBD)','Serial GND (pin TBD)','Serial reference','ground')],'MicroSquirt external serial requires the matching electrical interface, not raw Pi TTL GPIO. Confirm cable and connector pinout; use one serial host at a time.')
s.bundle('ECU adapter / dash link','Serial interface / BCM','BCM Controller / FoxbodyDash',[row('USB connector','USB host','Standard ECU serial-adapter cable','bus'),row('Network endpoint','Dash network endpoint','Local API/network link (not GPIO)','bus')])
s.bundle('LIN sensor wiring','Rain sensor (pinout TBD)','LIN Adapter LIN-01',[row('LIN (verify)','LIN','Single-wire LIN bus','bus'),row('Supply (TBD)','Rated vehicle supply (TBD)','Confirm sensor voltage before power','power'),row('Ground (verify)','GND','LIN reference','ground')])
s.bundle('LIN logic interface','BCM / protected serial logic','LIN Adapter LIN-01',[row('TX (GPIO TBD)','TX (verify)','Logic transmit • voltage compatibility TBD','bus'),row('RX (GPIO TBD)','RX (verify)','Logic receive • level protection TBD','bus'),row('Enable (GPIO TBD)','SLP (verify)','Sleep/enable polarity TBD','signal'),row('Logic GND','GND','Logic reference','ground')],'VIN, INH, TX/RX and SLP functions must be verified for this exact module. INH is not an arbitrary sensor power feed. Final LIN power wiring remains unresolved.')
s.bundle('TPMS / future peripherals','TPMS receiver / optional devices','BCM Controller',[row('Interface (TBD)','Host port (TBD)','USB / serial type not selected','bus')])
s.notes(['ADC/front-end choice, sensor supplies, protection, shield drains and connector pins are still open decisions. Physical analog pin numbers must not be guessed.','Fuel calibration: near empty, known added-gallon points and full; filter slosh before publishing. MicroSquirt remains engine-control authority.','Phone proximity uses BCM radio; no physical wire. GPS/cellular are future options. Steering-wheel/Pico wiring is outside this existing ten-sheet set.']); s.save()

if __name__ == '__main__':
 print(f'Regenerated {len(list(OUT.glob("*.svg")))} SVG schematics in {OUT}')
