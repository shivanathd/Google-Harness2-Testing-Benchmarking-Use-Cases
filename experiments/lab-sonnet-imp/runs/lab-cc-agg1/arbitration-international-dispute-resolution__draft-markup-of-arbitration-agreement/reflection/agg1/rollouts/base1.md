[ASSISTANT] I'll start by looking at what's in the data room and the helper scripts.
[ACTION] Bash {"command": "pwd; ls -la; echo ---; ls -la documents scripts output 2>&1", "description": "List workspace, documents, scripts, output"}
[OBSERVATION]
.
total 8
drwxr-xr-x@ 6 me  staff   192 Oct 19 11:47 .
drwxr-xr-x@ 3 me  staff    96 Oct 19 11:47 ..
-rw-r--r--@ 1 me  staff  1378 Oct 19 11:47 CLAUDE.md
drwxr-xr-x@ 6 me  staff   192 Oct 19 10:40 documents
drwxr-xr-x@ 2 me  staff    64 Oct 19 11:47 output
drwxr-xr-x@ 3 me  staff    96 Oct 19 11:47 scripts
---
documents:
total 232
drwxr-xr-x@ 6 me  staff    192 Oct 19 10:40 .
drwxr-xr-x@ 6 me  staff    192 Oct 19 11:47 ..
-rw-r--r--@ 1 me  staff   5115 Oct 19 10:40 cascadian-counsel-cover-email.eml
-rw-r--r--@ 1 me  staff  44268 Oct 19 10:40 proposed-arbitration-agreement.docx
-rw-r--r--@ 1 me  staff  55877 Oct 19 10:40 whitmore-arbitration-playbook.docx
-rw-r--r--@ 1 me  staff   7716 Oct 19 10:40 whitmore-internal-instructions.eml

output:
total 0
drwxr-xr-x@ 2 me  staff   64 Oct 19 11:47 .
drwxr-xr-x@ 6 me  staff  192 Oct 19 11:47 ..

scripts:
total 8
drwxr-xr-x@ 3 me  staff   96 Oct 19 11:47 .
drwxr-xr-x@ 6 me  staff  192 Oct 19 11:47 ..
-rw-r--r--@ 1 me  staff  482 Oct 19 11:47 read_doc.py
[ACTION] Bash {"command": "cd .; cat scripts/read_doc.py; echo ---EML1; cat documents/cascadian-counsel-cover-email.eml; echo ---EML2; cat documents/whitmore-internal-instructions.eml", "description": "Read helper script and the two email files"}
[ACTION] Bash {"command": "cd .; python3 -I scripts/read_doc.py documents/proposed-arbitration-agreement.docx > /tmp/proposed.txt 2>&1; python3 -I scripts/read_doc.py documents/whitmore-arbitration-playbook.docx > /tmp/playbook.txt 2>&1; wc -c /tmp/proposed.txt /tmp/playbook.txt", "description": "Extract text from the two .docx documents to temp files"}
[OBSERVATION]
#!/usr/bin/env python3
"""Print the text of a document: python3 scripts/read_doc.py <path>"""
import subprocess, sys
from pathlib import Path
p = Path(sys.argv[1])
if p.suffix.lower() == ".docx":
    r = subprocess.run(["pandoc", str(p), "-t", "markdown", "--wrap=none",
                        "--track-changes=all"], capture_output=True, text=True)
    sys.stdout.write(r.stdout); sys.stderr.write(r.stderr); sys.exit(r.returncode)
sys.stdout.write(p.read_text(errors="replace"))
---EML1
From: Margaret Hsiao <mhsiao@pinnaclebracewell.com>
To: David Ostrander <dostrander@hargovewynncalloway.com>
Cc: Thomas Riordan <triordan@cascadiangrowth.com>
Date: Wed, 08 Jan 2025 03:47:00 -0000
Subject: Vantage Specialty Chemicals — Proposed Arbitration Agreement (Exhibit
 F to Co-Investment Agreement)
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: quoted-printable
MIME-Version: 1.0

David,

I hope the new year is off to a good start for you and your team. I am writin=
g in connection with the ongoing negotiations regarding the co-investment by =
Cascadian Growth Fund LP ("Cascadian") and Whitmore Capital Fund III LP ("Whi=
tmore") in connection with the proposed acquisition of Vantage Specialty Chem=
icals Inc. Specifically, I am circulating for your review the proposed form o=
f arbitration agreement, which will be attached to the Co-Investment Agreemen=
t as Exhibit F. This draft was prepared at the direction of Thomas Riordan, G=
eneral Counsel of Cascadian Growth Management LLC, who is copied here.

Please find attached a clean draft of the proposed Arbitration Agreement betw=
een Cascadian Growth Fund LP and Whitmore Capital Fund III LP (in Word format=
 for ease of markup). The agreement is intended to govern the resolution of a=
ny disputes arising under or in connection with the Co-Investment Agreement. =
We have structured it as a standalone agreement that will be incorporated by =
reference as Exhibit F to the CIA.

By way of a brief summary, the proposed terms reflect Cascadian's standard ap=
proach for co-investment arrangements of this nature. The agreement provides =
for arbitration administered by the International Chamber of Commerce (ICC), =
with the seat of arbitration in Seattle, Washington. It contemplates the appo=
intment of a sole arbitrator, and the agreement itself is governed by Washing=
ton state law. These terms are consistent with Cascadian's customary practice=
 for dispute resolution in co-investment transactions, and we believe they pr=
ovide a balanced and efficient framework for both parties.

The scope clause is drafted broadly to cover disputes arising under both the =
Arbitration Agreement itself and the Co-Investment Agreement, including issue=
s of formation, validity, interpretation, performance, breach, and terminatio=
n. The agreement also addresses discovery procedures, consolidation, joinder =
of third parties, fees and costs allocation, limitations period, award timeli=
ne, and post-arbitration document handling. We have intentionally kept the ag=
reement streamlined and have relied on the ICC Rules to fill procedural gaps =
where appropriate, rather than building in additional procedural machinery th=
at we believe would add complexity without proportionate benefit in a two-par=
ty co-investment context.

We would welcome the opportunity for your team to review the proposed form an=
d provide a redlined markup with any comments or proposed revisions. Given th=
e parties' target of executing the Co-Investment Agreement on January 15, 202=
5, and the need to finalize all exhibits in advance of execution, we would ap=
preciate receiving your markup by end of business on Monday, January 13, 2025=
. Once we have your comments in hand, I am happy to schedule a call to discus=
s any significant points of divergence. I should also note that Thomas is cop=
ied here and is available to discuss commercial points directly with Rebecca =
Stadler at Whitmore if that would be helpful in resolving any open items effi=
ciently.

As you know, the parties are working toward an expected closing of March 31, =
2025, and we are concurrently working through comments on the other CIA exhib=
its in parallel. I understand the target management presentation is scheduled=
 for February 5, 2025, and finalizing the CIA =E2=80=94 including Exhibit F =
=E2=80=94 in advance of that date would be beneficial to both sides. Given th=
e collaborative nature of the co-investment, I am confident we can work throu=
gh any comments on the arbitration provisions efficiently.

Please don't hesitate to reach out if you have any preliminary questions befo=
re circulating your markup. We look forward to working with you and your team=
 on this.

Best regards,

Margaret Hsiao
Partner
Pinnacle Winterhaven LLP
999 Third Avenue, Suite 4200
Seattle, WA 98104
Tel: (206) 555-3180
Email: mhsiao@pinnaclebracewell.com

---

CONFIDENTIALITY NOTICE: This email message and any attachments are intended s=
olely for the use of the addressee(s) named above and may contain information=
 that is privileged, confidential, and/or exempt from disclosure under applic=
able law, including attorney-client privileged communications and attorney wo=
rk product. If you are not the intended recipient, you are hereby notified th=
at any dissemination, distribution, copying, or other use of this message or =
its attachments is strictly prohibited. If you have received this communicati=
on in error, please notify the sender immediately by reply email and permanen=
tly delete the original message and all copies. Thank you.
---EML2
From: David Ostrander <dostrander@hargrovewynn.com>
To: Priya Nakamura <pnakamura@hargrovewynn.com>
Date: Thu, 09 Jan 2025 11:03:00 -0000
Subject: FW: Vantage / Cascadian Co-Investment — Arbitration Agreement Review
 Priorities
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: quoted-printable
MIME-Version: 1.0

Priya,

Forwarding the below exchange with Rebecca Stadler, GC at Whitmore Capital Pa=
rtners, regarding the Vantage Specialty Chemicals / Cascadian Growth Fund co-=
investment. Pinnacle Winterhaven (Margaret Hsiao) circulated a proposed arbitra=
tion agreement =E2=80=94 Exhibit F to the Co-Investment Agreement =E2=80=94 o=
n January 8. We need a full markup.

Deliverables: (1) redlined markup of the proposed agreement with bracketed co=
mments explaining each change, referencing the playbook, and categorizing eve=
ry position as Required, Preferred, or Fallback; and (2) a cover memo summari=
zing all changes by priority tier (critical, important, recommended) with bri=
ef legal and commercial rationale.

Source materials: the proposed agreement and the Whitmore Arbitration Playboo=
k (November 2024 version =E2=80=94 should be in the deal folder on the DMS). =
Rebecca's email below highlights her three highest-priority items. The playbo=
ok is your baseline for everything else.

Rebecca's three priorities in short: (1) Three-member panel =E2=80=94 sole ar=
bitrator is a non-starter at this deal size ($325M equity); standard selectio=
n mechanics required. (2) Delete the waiver of court interim relief entirely =
=E2=80=94 non-negotiable =E2=80=94 and add emergency arbitrator provisions. (=
3) Insert expedited procedures for capital call, drag-along, and buy-sell dis=
putes with a 45-day award deadline.

Beyond those three, run the entire agreement against the playbook. I expect s=
ignificant deviations =E2=80=94 the form was drafted by Cascadian's counsel a=
nd is tilted their way across the board. Every deviation gets marked up with =
a comment.

Timeline: I need your draft redline and cover memo by Saturday, January 11, C=
OB so I can review before we send to Rebecca on Sunday. Final goes to Pinnacl=
e Winterhaven by January 13.

Tone guidance: thorough but professional. This is a co-investment relationshi=
p, not hostile litigation. Where the playbook identifies a fallback position,=
 note it in the comment so Rebecca can see room for negotiation.

Let me know if you have any questions or if you can't find the playbook in th=
e system =E2=80=94 I can send it over. Available by cell if you need to discu=
ss.

David

David Ostrander
Partner
Hargrove, Wynn & Calloway LLP

---

From: David Ostrander <dostrander@hargrovewynn.com>
To: Rebecca Stadler <rstadler@whitmorecapital.com>
Date: Thursday, January 9, 2025, 10:42 AM EST
Subject: RE: Vantage / Cascadian Co-Investment =E2=80=94 Arbitration Agreemen=
t Review Priorities

Rebecca,

Thanks for the clear direction =E2=80=94 we're aligned on all three priority =
items.

I'm assigning the full markup to Priya Nakamura, a senior associate on the de=
al team who has worked on several arbitration agreement reviews for Whitmore =
and knows the playbook well. She'll run the Cascadian form against the Novemb=
er 2024 playbook top to bottom and flag every deviation with comments explain=
ing the playbook basis and categorizing positions as Required, Preferred, or =
Fallback.

We'll have a draft redline and cover memo to you by end of day Sunday, Januar=
y 12, for your review before it goes to Pinnacle Winterhaven on the 13th.

The ICC designation and Seattle seat jumped out to me as well =E2=80=94 class=
ic counterparty home-cooking. Those will be addressed per the playbook (AAA f=
or domestic transactions, Atlanta as primary seat with New York as a brackete=
d fallback).

One question: do you want me to call Thomas Riordan or Margaret Hsiao directl=
y to give a heads-up on the scope of the markup, or would you prefer to let t=
he redline speak for itself? Given the number of changes I anticipate, a cour=
tesy call might smooth the path.

We'll get this turned around quickly. Talk soon.

David

David Ostrander
Partner
Hargrove, Wynn & Calloway LLP
195 Peachtree Street NE, Suite 4500
Atlanta, GA 30303
(404) 555-0178
dostrander@hargrovewynn.com

---

From: Rebecca Stadler <rstadler@whitmorecapital.com>
To: David Ostrander <dostrander@hargrovewynn.com>
Date: Thursday, January 9, 2025, 8:17 AM EST
Subject: Vantage / Cascadian Co-Investment =E2=80=94 Arbitration Agreement Re=
view Priorities

David,

I've reviewed the proposed arbitration agreement (Exhibit F to the Co-Investm=
ent Agreement) that Margaret Hsiao at Pinnacle Winterhaven circulated yesterday=
 on behalf of Cascadian Growth Fund LP. I have a number of concerns and want =
to flag my top priorities before your team begins the full markup.

First =E2=80=94 the sole arbitrator provision is unacceptable. Whitmore Capit=
al Fund III LP is committing $195 million in equity to the Vantage Specialty =
Chemicals acquisition, and the total equity check between the two parties is =
$325 million. Our playbook threshold for a three-member panel is $10 million =
=E2=80=94 we're more than 30x over that threshold. This is a hard no. The mar=
kup must require a three-member panel with standard selection mechanics: each=
 side picks one arbitrator, the two party-appointed arbitrators select the ch=
air. Do not present this as a "preferred" position. It is required.

Second =E2=80=94 I noticed the proposed agreement includes an express waiver =
of the right to seek provisional or interim measures from any court of compet=
ent jurisdiction. This is non-negotiable. Whitmore must preserve the ability =
to go to court for injunctive or provisional relief, particularly in scenario=
s involving breaches of exclusivity, unauthorized transfers, or confidentiali=
ty violations. In the Fund II co-investment, we had a situation where we need=
ed emergency TRO relief and it was critical that the arbitration agreement di=
dn't foreclose that option. Delete the waiver entirely and replace it with a =
carve-out preserving both court-ordered interim relief and emergency arbitrat=
or procedures.

Third =E2=80=94 expedited arbitration procedures for capital call disputes, d=
rag-along rights, and buy-sell provisions are critical for fund governance. C=
apital call disputes cannot sit in a standard arbitration timeline =E2=80=94 =
if a co-investor disputes a capital call, the fund needs resolution within we=
eks, not months. The playbook requires a 45-day expedited track for these cat=
egories of disputes, and I want that reflected in the markup. Cascadian's for=
m has no expedited procedure carve-out at all. Our investment committee has s=
pecifically focused on this given the size of the equity commitment and the g=
overnance dynamics with a co-investor holding a 24% stake.

Beyond these three items, the full arbitration playbook (last updated Novembe=
r 2024) should govern the markup on all other points. I expect there will be =
additional issues =E2=80=94 the form looks like it was drafted entirely from =
Cascadian's perspective (Seattle as the seat, ICC as the administering instit=
ution, Washington state law). I trust the team to run it against the playbook=
 comprehensively. The markup is due back to Pinnacle Winterhaven by January 13,=
 and I need time to review before it goes out. Please get me a draft by end o=
f day Sunday, January 12.

Let me know if you have questions. Happy to jump on a call if helpful.

Rebecca

Rebecca Stadler
General Counsel
Whitmore Capital Partners LLC
3400 Peachtree Road NE, Suite 1200
Atlanta, GA 30326
(404) 555-0243
rstadler@whitmorecapital.com
[OBSERVATION]
   16061 /tmp/proposed.txt
   45338 /tmp/playbook.txt
   61399 total
[ASSISTANT] The internal instructions point to a Whitmore-side markup. Next I'll read the proposed agreement and the playbook in full.
[ACTION] Read {"file_path": "/tmp/proposed.txt"}
[OBSERVATION]
1	**EXHIBIT F TO CO-INVESTMENT AGREEMENT**
2	
3	**ARBITRATION AGREEMENT**
4	
5	Dated as of January 15, 2025
6	
7	This Arbitration Agreement (this \"**Agreement**\") is entered into as of January 15, 2025, by and between the following parties in connection with that certain Co-Investment Agreement dated as of even date herewith (the \"**Co-Investment Agreement**\"). Capitalized terms used but not otherwise defined herein shall have the meanings ascribed to them in the Co-Investment Agreement.
8	
9	**[RECITALS]{.underline}**
10	
11	**WHEREAS**, Whitmore Capital Fund III LP, a Delaware limited partnership (\"**Whitmore**\"), an investment vehicle managed by Whitmore Capital Partners LLC, a Delaware limited liability company, with its principal office at 3400 Peachtree Road NE, Suite 1200, Atlanta, GA 30326, and Cascadian Growth Fund LP, a Delaware limited partnership (\"**Cascadian**\"), managed by its general partner, Cascadian Growth Management LLC, a Delaware limited liability company, with its principal office at 1501 Fourth Avenue, Suite 3700, Seattle, WA 98101 (each, a \"**Party**\" and together, the \"**Parties**\"), have entered into that certain Co-Investment Agreement dated as of January 15, 2025 (the \"**Co-Investment Agreement**\");
12	
13	**WHEREAS**, pursuant to the Co-Investment Agreement, the Parties have agreed to jointly acquire a controlling interest (approximately 72%) of Vantage Specialty Chemicals Inc., a Delaware corporation headquartered at 10200 Bellaire Boulevard, Suite 400, Houston, TX 77072 (the \"**Target**\" or the \"**Company**\"), at a total enterprise value of \$680,000,000, with Whitmore contributing \$195,000,000 in equity for a 48% equity stake and Cascadian contributing \$130,000,000 in equity for a 24% equity stake, for total equity of \$325,000,000, with the remaining \$355,000,000 in debt financing;
14	
15	**WHEREAS**, the Co-Investment Agreement governs, among other things, governance rights, drag-along and tag-along rights, transfer restrictions, and capital call mechanics relating to the Parties\' investment in the Company; and
16	
17	**WHEREAS**, the Parties desire to establish the terms and procedures by which disputes arising under or in connection with the Co-Investment Agreement shall be resolved.
18	
19	**NOW, THEREFORE**, in consideration of the mutual covenants and agreements set forth in the Co-Investment Agreement, and for other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the Parties agree as follows:
20	
21	**[ARTICLE I --- DEFINITIONS]{.underline}**
22	
23	As used in this Agreement, the following terms shall have the meanings set forth below:
24	
25	\"**Agreement**\" means this Arbitration Agreement, as it may be amended from time to time in accordance with its terms.
26	
27	\"**Arbitral Tribunal**\" or \"**Tribunal**\" means the arbitrator or arbitrators appointed pursuant to Article IV of this Agreement to resolve a Dispute.
28	
29	\"**Award**\" means any interim, partial, or final award rendered by the Arbitral Tribunal in connection with any Proceedings.
30	
31	\"**Claimant**\" means the Party initiating a Proceeding by filing a request for arbitration.
32	
33	\"**Co-Investment Agreement**\" or \"**CIA**\" has the meaning set forth in the Recitals.
34	
35	\"**Company**\" means Vantage Specialty Chemicals Inc., a Delaware corporation.
36	
37	\"**Dispute**\" means any dispute, controversy, or claim arising out of, relating to, or in connection with this Agreement or the Co-Investment Agreement, including any question regarding the existence, formation, validity, interpretation, performance, breach, or termination thereof.
38	
39	\"**ICC**\" means the International Chamber of Commerce.
40	
41	\"**ICC Rules**\" means the Rules of Arbitration of the International Chamber of Commerce in effect at the time of commencement of the arbitration.
42	
43	\"**Party**\" and \"**Parties**\" have the meanings set forth in the Recitals.
44	
45	\"**Proceedings**\" means any arbitration proceedings commenced pursuant to this Agreement.
46	
47	\"**Respondent**\" means the Party against whom a request for arbitration is filed.
48	
49	\"**Seat**\" means Seattle, Washington, which shall be the juridical seat of any arbitration conducted under this Agreement.
50	
51	**[ARTICLE II --- AGREEMENT TO ARBITRATE; SCOPE]{.underline}**
52	
53	**Section 2.1 --- Agreement to Arbitrate.** Any and all disputes, controversies, or claims arising out of, relating to, or in connection with this Agreement or the Co-Investment Agreement, including but not limited to the formation, validity, interpretation, performance, breach, or termination thereof (each, a \"**Dispute**\"), shall be exclusively and finally resolved by binding arbitration administered by the International Chamber of Commerce in accordance with the ICC Rules in effect at the time of the filing of the request for arbitration. The Parties acknowledge and agree that this Agreement evidences a transaction involving commerce and that the Federal Arbitration Act, 9 U.S.C. §§ 1--16, shall govern the interpretation and enforcement of this Agreement.
54	
55	**Section 2.2 --- Exclusive Remedy.** Arbitration under this Agreement shall be the exclusive remedy for any Dispute, and no Party shall institute any action or proceeding in any court with respect to any Dispute, except as expressly provided herein.
56	
57	**[ARTICLE III --- SEAT, LANGUAGE, AND GOVERNING LAW]{.underline}**
58	
59	**Section 3.1 --- Seat of Arbitration.** The seat (legal place) of arbitration shall be Seattle, Washington. Any hearings shall be conducted at the Seat unless otherwise agreed by the Parties or ordered by the Arbitral Tribunal.
60	
61	**Section 3.2 --- Language.** The language of the arbitration shall be English. All submissions, correspondence, evidence, and hearings shall be conducted in English.
62	
63	**Section 3.3 --- Governing Law.** This Agreement shall be governed by and construed in accordance with the laws of the State of Washington, without regard to its conflict of laws principles.
64	
65	**[ARTICLE IV --- ARBITRATOR APPOINTMENT AND QUALIFICATIONS]{.underline}**
66	
67	**Section 4.1 --- Number of Arbitrators.** The arbitration shall be conducted by a sole arbitrator (the \"**Arbitrator**\") appointed in accordance with the ICC Rules.
68	
69	**Section 4.2 --- Appointment Procedure.** The Parties shall endeavor to agree upon a mutually acceptable Arbitrator within thirty (30) days following the filing of the request for arbitration. If the Parties are unable to agree upon the Arbitrator within such thirty (30)-day period, the Arbitrator shall be appointed by the ICC in accordance with the ICC Rules.
70	
71	**Section 4.3 --- Qualifications.** The Arbitrator shall be a neutral individual independent of the Parties.
72	
73	**[ARTICLE V --- ARBITRATION PROCEDURES]{.underline}**
74	
75	**Section 5.1 --- Discovery.** Discovery shall be conducted in accordance with the ICC Rules, without modification. The Arbitrator shall have the authority to manage and limit discovery as the Arbitrator deems appropriate in the interests of efficiency and proportionality.
76	
77	**Section 5.2 --- Hearings.** The Arbitrator shall hold hearings as the Arbitrator deems necessary and appropriate. Hearings shall be held at the Seat unless otherwise agreed by the Parties or directed by the Arbitrator.
78	
79	**Section 5.3 --- Evidence.** The Arbitrator shall have the authority to receive and consider such evidence as the Arbitrator deems relevant and material, including documentary evidence, witness testimony, and expert reports. The Arbitrator shall determine the admissibility, relevance, materiality, and weight of any evidence offered.
80	
81	**[ARTICLE VI --- INTERIM AND EMERGENCY RELIEF]{.underline}**
82	
83	**Section 6.1 --- Waiver of Court Relief.** The Parties hereby expressly waive any right to seek provisional or interim measures, including but not limited to temporary restraining orders, preliminary injunctions, attachments, or any other form of interim or conservatory relief, from any court of competent jurisdiction in connection with any Dispute subject to arbitration under this Agreement. All requests for provisional or interim measures shall be directed exclusively to the Arbitral Tribunal. The Parties acknowledge that this waiver is knowing, voluntary, and made in consideration of the mutual benefits of resolving all aspects of any Dispute through the arbitral process established herein.
84	
85	**[ARTICLE VII --- CONSOLIDATION AND JOINDER]{.underline}**
86	
87	**Section 7.1 --- Consolidation.** The Tribunal may, at the request of either Party, consolidate this arbitration with any other arbitration arising out of or in connection with the Co-Investment Agreement or any other agreement between the Parties or involving a party to this Agreement, provided that the Tribunal determines that common questions of fact or law exist. The Tribunal shall have sole discretion to determine whether consolidation is appropriate and shall consider the stage of the existing proceedings, the efficiency of consolidation, and any prejudice to the Parties.
88	
89	**Section 7.2 --- Joinder of Third Parties.** Third parties may be joined to the arbitration at the discretion of the Tribunal, upon request by either Party, without the requirement of consent of all parties to the arbitration or of the party to be joined, provided that the Tribunal determines that such joinder is necessary for the complete resolution of the Dispute. The Tribunal shall have full authority to establish the terms and conditions of any such joinder, including with respect to the allocation of costs associated therewith.
90	
91	**[ARTICLE VIII --- AWARD]{.underline}**
92	
93	**Section 8.1 --- Timing and Form of Award.** The Arbitrator shall use best efforts to issue a reasoned award within one hundred twenty (120) days of the close of Proceedings. The award shall be in writing and shall set forth the Arbitrator\'s reasoning. Failure to render the award within such period shall not affect the validity of the award or the jurisdiction of the Arbitrator.
94	
95	**Section 8.2 --- Finality.** The award of the Arbitrator shall be final and binding upon the Parties and shall not be subject to appeal, except as otherwise provided by applicable law. Judgment upon the award may be entered in any court of competent jurisdiction. The Parties hereby waive, to the fullest extent permitted by law, any right to appeal or challenge the award, except on the limited grounds set forth in the Federal Arbitration Act.
96	
97	**Section 8.3 --- Remedies.** The Arbitrator shall have the authority to award any remedy or relief that a court of competent jurisdiction could grant, including but not limited to specific performance, injunctive relief, and monetary damages. The Arbitrator shall not be limited in the types or amounts of damages that may be awarded.
98	
99	**[ARTICLE IX --- COSTS AND FEES]{.underline}**
100	
101	**Section 9.1 --- Allocation of Costs.** Each Party shall bear its own costs and expenses of the arbitration, including but not limited to attorneys\' fees, expert fees, witness fees, and all other costs incurred in connection with the arbitration, regardless of the outcome.
102	
103	**Section 9.2 --- Administrative Costs.** The administrative fees and expenses of the ICC and the fees and expenses of the Arbitrator shall be shared equally by the Parties, unless the Arbitrator determines otherwise in the award.
104	
105	**[ARTICLE X --- LIMITATIONS PERIOD]{.underline}**
106	
107	**Section 10.1 --- Statute of Limitations.** All claims subject to arbitration under this Agreement must be commenced by the filing of a request for arbitration within one (1) year of the date on which the claiming Party knew or should have known of the facts giving rise to the claim. Any claim not commenced within such one (1)-year period shall be forever barred and waived. The Parties acknowledge that this limitations period may be shorter than the limitations period otherwise applicable under governing law and agree that this shortened period is reasonable and enforceable.
108	
109	**[ARTICLE XI --- DOCUMENT RETENTION AND DESTRUCTION]{.underline}**
110	
111	**Section 11.1 --- Post-Arbitration Document Handling.** The Parties agree that, within thirty (30) days following the issuance of the final award (or, if applicable, the resolution of any proceeding to confirm or vacate the award), each Party shall destroy or cause to be destroyed all documents, materials, evidence, submissions, transcripts, and other records produced, created, or exchanged during the arbitration, and shall certify such destruction in writing to the other Party. This obligation shall survive the termination of this Agreement and shall be binding upon each Party\'s officers, directors, employees, agents, and representatives.
112	
113	**[ARTICLE XII --- GENERAL PROVISIONS]{.underline}**
114	
115	**Section 12.1 --- Notices.** All notices, requests, demands, and other communications under this Agreement shall be delivered in the manner provided in Section 11.4 of the Co-Investment Agreement to the Parties at the addresses set forth therein or such other address as a Party may designate in writing from time to time in accordance with the provisions of the Co-Investment Agreement.
116	
117	**Section 12.2 --- Entire Agreement.** This Agreement constitutes the entire agreement between the Parties with respect to the subject matter hereof and supersedes all prior negotiations, representations, warranties, commitments, offers, and agreements (whether oral or written) with respect to the subject matter hereof.
118	
119	**Section 12.3 --- Amendment and Waiver.** This Agreement may not be amended, modified, or supplemented except by a written instrument signed by both Parties. No waiver of any provision of this Agreement shall be effective unless in writing signed by the waiving Party. No failure or delay by any Party in exercising any right, power, or privilege hereunder shall operate as a waiver thereof, nor shall any single or partial exercise thereof preclude any other or further exercise thereof or the exercise of any other right, power, or privilege.
120	
121	**Section 12.4 --- Severability.** If any provision of this Agreement is held to be invalid, illegal, or unenforceable in any respect, such invalidity, illegality, or unenforceability shall not affect any other provision of this Agreement, and this Agreement shall be construed as if such invalid, illegal, or unenforceable provision had never been contained herein. The Parties shall negotiate in good faith to replace any such invalid, illegal, or unenforceable provision with a valid, legal, and enforceable provision that, to the greatest extent possible, achieves the original intent and economic effect of the invalid provision.
122	
123	**Section 12.5 --- Counterparts.** This Agreement may be executed in counterparts, each of which shall be deemed an original, and all of which together shall constitute one and the same instrument. Execution and delivery of this Agreement by facsimile or electronic transmission (including in .pdf format) shall be deemed to be, and shall have the same legal effect as, execution and delivery of an original.
124	
125	**Section 12.6 --- Relationship to Co-Investment Agreement.** This Agreement is Exhibit F to and is incorporated into the Co-Investment Agreement. In the event of a conflict between the terms of this Agreement and the arbitration-related provisions of the Co-Investment Agreement, the terms of this Agreement shall control.
126	
127	**Section 12.7 --- Survival.** This Agreement shall survive the termination or expiration of the Co-Investment Agreement with respect to any Dispute arising prior to or upon such termination or expiration.
128	
129	*\[Signature Page Follows\]*
130	
131	**IN WITNESS WHEREOF**, the Parties have executed this Arbitration Agreement as of the date first written above.
132	
133	**WHITMORE CAPITAL FUND III LP**
134	
135	By: Whitmore Capital Partners LLC, its General Partner
136	
137	By: **\_\_\_\_\_\_\_\_**
138	
139	Name: **\_\_\_\_\_\_\_\_**
140	
141	Title: **\_\_\_\_\_\_\_\_**
142	
143	Date: **\_\_\_\_\_\_\_\_**
144	
145	**CASCADIAN GROWTH FUND LP**
146	
147	By: Cascadian Growth Management LLC, its General Partner
148	
149	By: **\_\_\_\_\_\_\_\_**
150	
151	Name: **\_\_\_\_\_\_\_\_**
152	
153	Title: **\_\_\_\_\_\_\_\_**
154	
155	Date: **\_\_\_\_\_\_\_\_**
156	
[ASSISTANT] Now the playbook, which is the baseline for the markup.
[ACTION] Read {"file_path": "/tmp/playbook.txt"}
[OBSERVATION]
1	**PRIVILEGED & CONFIDENTIAL --- ATTORNEY-CLIENT PRIVILEGED / WORK PRODUCT**
2	
3	**[WHITMORE CAPITAL PARTNERS LLC]{.underline}**
4	
5	**[ARBITRATION PLAYBOOK: POLICY & GUIDANCE FOR OUTSIDE COUNSEL]{.underline}**
6	
7	**From:** Rebecca Stadler, General Counsel Whitmore Capital Partners LLC 3400 Peachtree Road NE, Suite 1200 Atlanta, GA 30326
8	
9	**To:** Outside Counsel Hargrove, Wynn & Calloway LLP 195 Peachtree Street NE, Suite 4500 Atlanta, GA 30303 *Attention:* David Ostrander, Partner; Priya Nakamura, Associate
10	
11	**Date:** Last Updated November 15, 2024
12	
13	**Version:** 3.0
14	
15	**Supersedes:** Version 2.0 (March 2022)
16	
17	**[Section 1: Purpose and Scope]{.underline}**
18	
19	This memorandum establishes Whitmore Capital Partners LLC\'s (\"Whitmore\" or the \"Firm\") mandatory policies, preferred positions, and acceptable fallback positions for arbitration provisions in transaction documents. It is intended to serve as a comprehensive reference for outside counsel when drafting, reviewing, negotiating, or marking up arbitration agreements and dispute resolution provisions.
20	
21	**Applicability.** This playbook applies to all arbitration agreements, arbitration clauses, and dispute resolution provisions in connection with investments made by Whitmore Capital Fund III LP or any other Whitmore-managed fund vehicle, including but not limited to co-investment agreements, joint venture agreements, side letters, limited partnership agreements, subscription agreements, and any ancillary agreements containing dispute resolution provisions.
22	
23	**Compliance Requirement.** Outside counsel must consult this playbook before drafting or reviewing any arbitration provision. Any departure from a position designated as \"Required\" must be flagged for approval by the General Counsel before acceptance. No Required position may be conceded in negotiations without express, prior written authorization from the General Counsel.
24	
25	**Organization.** This playbook is organized by topic. Each topic designates positions according to the following classification hierarchy:
26	
27	> • **Required** --- Non-negotiable absent General Counsel approval. These positions reflect Whitmore\'s firm policy and may not be compromised without escalation.
28	>
29	> • **Preferred** --- Target position in negotiations. Outside counsel should pursue these positions vigorously but may accept a Fallback position if necessary without escalation.
30	>
31	> • **Fallback** --- Acceptable compromise if the Required or Preferred position cannot be obtained through negotiation.
32	
33	**Context.** Whitmore manages approximately \$3.8 billion in committed capital across three fund vehicles. The Firm\'s typical co-investment transaction sizes range from \$100 million to \$500 million in equity commitments. The stakes in arbitrated disputes arising from these transactions can be substantial, and the procedural framework governing those disputes has a material impact on outcomes. This playbook is designed to protect fund investors and ensure procedural fairness in every arbitrated dispute.
34	
35	**[Section 2: Administering Institution]{.underline}**
36	
37	**Required:** For all domestic U.S. transactions --- including co-investment agreements, joint venture agreements, and side letters --- the administering institution must be the **American Arbitration Association (\"AAA\")** under the **Commercial Arbitration Rules**.
38	
39	**Preferred:** AAA Commercial Arbitration Rules (most current version as of the date the dispute is submitted to arbitration).
40	
41	**Fallback:** JAMS Comprehensive Arbitration Rules and Procedures is acceptable as an alternative if the counterparty objects to AAA. JAMS provides a credible domestic commercial arbitration platform with a qualified roster of arbitrators.
42	
43	**NOT ACCEPTABLE:** The International Chamber of Commerce (\"ICC\") is reserved exclusively for cross-border or international transactions --- that is, transactions in which at least one party is organized or headquartered outside the United States, or the underlying assets are located outside the United States. The ICC shall **never** be designated as the administering institution for purely domestic U.S. co-investment transactions.
44	
45	**Rationale:**
46	
47	> • AAA has the deepest bench of domestic commercial arbitrators with private equity, mergers and acquisitions, and corporate finance experience.
48	>
49	> • ICC administrative fees are disproportionately high for domestic matters, as they are calculated based on the amount in dispute using fee scales designed for international proceedings.
50	>
51	> • ICC procedural rules are designed for international disputes and introduce unnecessary complexity in domestic contexts, including requirements such as the Terms of Reference, the ICC Court\'s scrutiny of draft awards, and other procedural mechanisms that add cost and delay without corresponding benefit in a purely domestic U.S. proceeding.
52	>
53	> • AAA\'s procedural framework is more streamlined for domestic commercial disputes, and its case management personnel are experienced with U.S. private equity and M&A matters.
54	
55	**[Section 3: Seat of Arbitration]{.underline}**
56	
57	**Required:** The seat (legal place) of arbitration must be **Atlanta, Georgia** --- Whitmore\'s home jurisdiction.
58	
59	**Preferred:** Atlanta, Georgia.
60	
61	**Fallback:** If the counterparty objects to Atlanta, **New York, New York** is acceptable as a neutral forum. New York provides a well-developed body of arbitration law under the New York Convention and the Federal Arbitration Act, and is generally perceived as a neutral commercial arbitration venue.
62	
63	**NOT ACCEPTABLE:** The counterparty\'s home jurisdiction. Under no circumstances should the seat be located in a jurisdiction where the counterparty (or its general partner or management company) is headquartered. This restriction is categorical and applies regardless of the counterparty\'s identity. Agreeing to the counterparty\'s home jurisdiction creates an inherent advantage for the counterparty in terms of familiarity with local courts (for enforcement, provisional relief, and vacatur proceedings), convenience for the counterparty\'s personnel and counsel, and potential perception of home-court bias.
64	
65	**Rationale:**
66	
67	> • The seat of arbitration determines the supervisory court for vacatur and enforcement proceedings under the Federal Arbitration Act, 9 U.S.C. §§ 1--16.
68	>
69	> • Whitmore\'s executives, internal documents, and primary counsel are located in Atlanta, and designating Atlanta as the seat reduces cost and disruption to fund operations.
70	>
71	> • New York is acceptable as a fallback because of the depth and sophistication of its judiciary, its extensive body of case law on arbitration, and its widely recognized neutrality as a dispute resolution forum.
72	
73	**Hearing Location Note:** The physical location of hearings may differ from the seat if mutually convenient, but the legal seat governs the procedural law applicable to the arbitration, including the standards for judicial review, vacatur, and enforcement.
74	
75	**[Section 4: Number of Arbitrators and Selection Mechanics]{.underline}**
76	
77	**Required:** For any dispute where the amount in controversy exceeds **\$10 million**, the arbitration must be conducted before a **three-member arbitral tribunal**. Given that Whitmore\'s typical transaction sizes range from \$100 million to \$500 million in equity, virtually all disputes arising from co-investment agreements will exceed this threshold.
78	
79	**Preferred:** Three-member panel with the following selection mechanics:
80	
81	> \(a\) Each party (or side, if multiple parties are aligned as claimant or respondent) shall appoint one arbitrator within thirty (30) days of the filing of the demand for arbitration.
82	>
83	> \(b\) The two party-appointed arbitrators shall jointly select the chair (presiding arbitrator) within twenty (20) days of their appointment.
84	>
85	> \(c\) If the two party-appointed arbitrators cannot agree on a chair within the twenty (20) day period, the administering institution (AAA, or JAMS if applicable) shall appoint the chair from its roster of qualified arbitrators.
86	
87	**Fallback:** A sole arbitrator is acceptable only for disputes where the amount in controversy is **\$10 million or less**. Even in such cases, the sole arbitrator must meet all of the qualification requirements set forth in Section 5.
88	
89	**Rationale:**
90	
91	> • A three-member panel provides a structural check against any single arbitrator\'s potential bias, error, or idiosyncratic interpretation of the governing documents.
92	>
93	> • Three-member panels are standard for high-value commercial disputes and are the prevailing norm in private equity and M&A arbitration.
94	>
95	> • Party appointment of co-arbitrators allows each side meaningful participation in tribunal composition, which enhances the perceived legitimacy and fairness of the process.
96	>
97	> • The \$10 million threshold is set deliberately low to ensure that panel composition applies to virtually all fund-level disputes. A dispute arising from a \$325 million co-investment, for example, plainly warrants a three-member panel.
98	
99	**[Section 5: Arbitrator Qualifications]{.underline}**
100	
101	**Required:** All arbitrators --- whether serving as a sole arbitrator or as a member of a three-member panel --- must satisfy **all** of the following minimum qualifications:
102	
103	> 1\. **Experience:** A minimum of **fifteen (15) years** of professional experience in **private equity, mergers and acquisitions, or corporate finance**. Qualifying experience includes practice as an attorney, investment banker, or financial advisor in these fields, or service as an arbitrator in disputes involving these fields.
104	>
105	> 2\. **Roster Membership:** The arbitrator must be a member of the roster (panel) of the administering institution --- i.e., AAA\'s National Roster of Arbitrators or, if the administering institution is JAMS, the JAMS panel of neutrals.
106	>
107	> 3\. **Conflict-Free:** The arbitrator must not have had any professional, financial, or personal relationship with any party to the arbitration, any affiliate of a party, or any counsel of record within the **prior five (5) years**. This lookback period applies to direct and indirect relationships, including but not limited to service as counsel, advisor, board member, investor, consultant, or arbitrator in a proceeding involving any party, any affiliate of a party, or any counsel of record.
108	
109	**Preferred:** In addition to the requirements above, Whitmore prefers arbitrators who have served as arbitrators in at least three (3) prior disputes involving private equity co-investment or joint venture agreements.
110	
111	**Fallback:** If the counterparty objects to the 15-year experience requirement, Whitmore will accept a minimum of **ten (10) years** of qualifying experience, but only with prior General Counsel approval.
112	
113	**Rationale:**
114	
115	> • Private equity co-investment disputes involve complex governance, valuation, and contractual interpretation issues that require specialized knowledge. Generalist commercial arbitrators may lack the sophistication to handle capital call mechanics, waterfall calculations, drag-along and tag-along provisions, management fee offsets, clawback obligations, and other PE-specific issues.
116	>
117	> • The 5-year conflict lookback is essential to ensure independence and impartiality given the interconnected nature of the private equity industry, where a relatively small number of firms, advisors, and counsel participate across overlapping transactions.
118	
119	**[Section 6: Governing Law]{.underline}**
120	
121	**Required:** The governing law of the arbitration agreement itself --- as well as the underlying co-investment agreement --- must be the **law of the State of Delaware**, without regard to conflict-of-laws principles.
122	
123	**Preferred:** Delaware law. Delaware is the jurisdiction of organization for most Whitmore fund vehicles and portfolio companies, has the most well-developed body of corporate and commercial law in the United States, and is the standard choice of law for private equity transactions.
124	
125	**Fallback:** **New York law** is acceptable as an alternative if the counterparty objects to Delaware. New York provides a similarly developed body of commercial law and a sophisticated judiciary with extensive experience interpreting complex financial agreements.
126	
127	**NOT ACCEPTABLE:** The counterparty\'s home-state law. Whitmore\'s policy **categorically prohibits** agreeing to have the arbitration agreement (or the underlying transaction documents) governed by the law of the state where the counterparty is headquartered. This prohibition avoids: (a) unfamiliarity with the governing law for Whitmore\'s counsel, (b) potential counterparty advantages arising from local law nuances or favorable precedent, and (c) inconsistency with the governing law of the underlying transaction documents, which are typically governed by Delaware law.
128	
129	**Rationale:**
130	
131	> • Consistency with the governing law of the co-investment agreement and related transaction documents (which, in virtually all Whitmore transactions, are governed by Delaware law).
132	>
133	> • Depth of Delaware case law on contractual interpretation, arbitrability, and enforceability of arbitration provisions.
134	>
135	> • Avoidance of the counterparty\'s home-court advantage.
136	
137	**Note on Statute of Limitations:** Outside counsel should be aware that Delaware has a **three (3) year** statute of limitations for breach of contract claims not under seal (10 Del. C. § 8106), while New York has a **six (6) year** statute of limitations for breach of contract claims (N.Y. C.P.L.R. § 213). These differences should be considered when negotiating contractual limitations periods. *See* Section 15 for Whitmore\'s policy on statute of limitations.
138	
139	**[Section 7: Scope of Arbitration]{.underline}**
140	
141	**Required:** The arbitration clause should cover **all disputes** arising out of, relating to, or in connection with the co-investment agreement and any ancillary agreements, including disputes regarding formation, validity, interpretation, performance, breach, and termination.
142	
143	Broad scope clauses are acceptable and standard. Whitmore does not impose any restriction on the breadth of the scope clause. A comprehensive scope clause reduces the risk of jurisdictional challenges and parallel court proceedings.
144	
145	**Note:** Even with a broad scope clause, certain categories of disputes are subject to expedited treatment under Section 17 of this playbook.
146	
147	**[Section 8: Discovery Limitations]{.underline}**
148	
149	**Required:** Discovery must be limited as follows:
150	
151	> • **Fact Depositions:** Each side may take up to **three (3) fact depositions**, each not to exceed **seven (7) hours** of testimony on the record.
152	>
153	> • **Document Requests:** Each side may serve up to **fifteen (15) document requests** (including subparts).
154	>
155	> • **Expert Discovery:** Each side may retain **one (1) testifying expert**. Expert reports must be exchanged **simultaneously** on a date set by the tribunal.
156	
157	**Preferred:** The specific limitations set forth above should be stated expressly in the arbitration agreement itself, rather than being left to the rules of the administering institution or the tribunal\'s discretion.
158	
159	**Fallback:** If the counterparty objects to specific numerical limits, agree that \"discovery shall be limited and proportional to the amounts in dispute, as determined by the tribunal\" --- but insist on the deposition cap (3 depositions per side) and expert cap (1 testifying expert per side) as non-negotiable minimums.
160	
161	**Rationale:**
162	
163	> • Unlimited or expansive discovery is the primary driver of cost and delay in arbitration. The limitations set forth above are calibrated to be sufficient for disputes of the complexity typical in co-investment matters while preventing the arbitration from devolving into *de facto* federal litigation discovery.
164	>
165	> • The simultaneous exchange of expert reports prevents gamesmanship and eliminates the tactical advantage of sequential rebuttal.
166	>
167	> • If a proposed arbitration agreement states only that discovery will follow the administering institution\'s rules \"without modification,\" this is **inadequate**. The playbook requires affirmative limitations to be incorporated into the agreement itself.
168	
169	**[Section 9: Confidentiality]{.underline}**
170	
171	**Required:** Every arbitration agreement must include a **mandatory confidentiality provision**. The absence of a confidentiality provision is unacceptable.
172	
173	The confidentiality provision must cover each of the following categories of information:
174	
175	> 1\. The existence of the arbitration proceeding.
176	>
177	> 2\. All submissions, briefs, motions, and pleadings filed in the arbitration.
178	>
179	> 3\. All evidence, testimony, exhibits, and documents produced or presented during the arbitration.
180	>
181	> 4\. All orders, rulings, and awards issued by the tribunal.
182	>
183	> 5\. All communications between the parties and the tribunal.
184	
185	**Required Exceptions (and only these exceptions):**
186	
187	> \(i\) Disclosures required by applicable law, regulation, or order of a court of competent jurisdiction, including but not limited to SEC reporting obligations, tax reporting, and regulatory inquiries.
188	>
189	> \(ii\) Disclosures necessary for the enforcement, confirmation, or vacatur of an arbitral award in proceedings before a court of competent jurisdiction.
190	>
191	> \(iii\) Disclosures to professional advisors --- including attorneys, accountants, and financial advisors --- who are subject to professional duties of confidentiality, provided that such advisors agree to be bound by the confidentiality obligations set forth in the arbitration agreement.
192	
193	**Preferred:** Include a liquidated damages provision for breach of confidentiality, or at minimum, an express right to seek injunctive relief (including emergency relief) for any breach or threatened breach of the confidentiality obligations.
194	
195	**Fallback:** If the counterparty resists the full scope set forth above, at minimum require confidentiality of (a) the award and (b) all financial information, trade secrets, and proprietary business information produced in the arbitration.
196	
197	**Rationale:**
198	
199	> • Whitmore\'s fund investors (limited partners) have explicit and implicit confidentiality expectations with respect to fund operations, performance, and disputes.
200	>
201	> • Public disclosure of arbitration proceedings could adversely affect deal flow, fund performance reporting, investor relations, and Whitmore\'s competitive position.
202	>
203	> • The exceptions are narrowly tailored to legal and regulatory necessity and do not authorize voluntary or discretionary disclosure.
204	
205	**[Section 10: Interim and Emergency Relief]{.underline}**
206	
207	**Required:** The arbitration agreement must **expressly preserve** each party\'s right to seek provisional, interim, or injunctive measures from **any court of competent jurisdiction** at any time before, during, or after the arbitration. This right must be stated as an **express carve-out** to the agreement to arbitrate and must make clear that seeking such relief does not constitute a waiver of the right to arbitrate.
208	
209	**Required:** The agreement must incorporate the administering institution\'s **emergency arbitrator provisions** (e.g., AAA\'s Optional Rules for Emergency Measures of Protection or JAMS\'s equivalent emergency relief procedures).
210	
211	**NOT ACCEPTABLE:** Any waiver, restriction, or limitation on a party\'s right to seek interim or provisional relief from a court. Express waivers of court-ordered provisional relief are **categorically prohibited** and must be **deleted** wherever found in a counterparty\'s proposed agreement.
212	
213	**Preferred:** Include a specific statement that seeking court-ordered interim relief does not waive the right to arbitrate, is not inconsistent with the agreement to arbitrate, and shall not be deemed a submission to the jurisdiction of the court for any purpose other than the relief sought.
214	
215	**Fallback:** None. This is a **non-negotiable** position. If the counterparty insists on a waiver of court relief, escalate to the General Counsel immediately. Do not accept any formulation that restricts, limits, conditions, or delays a party\'s right to seek court-ordered provisional measures.
216	
217	**Rationale:**
218	
219	> • Provisional court relief --- such as temporary restraining orders, preliminary injunctions, and asset-freezing orders --- may be necessary on an emergency basis to prevent irreparable harm before an arbitral tribunal can be constituted. Common scenarios in the co-investment context include:
220	>
221	> \(a\) Breach of non-compete or non-solicitation provisions by portfolio company management.
222	>
223	> \(b\) Unauthorized transfer of equity interests in violation of transfer restrictions, ROFR provisions, or lock-up periods.
224	>
225	> \(c\) Misappropriation of confidential information, trade secrets, or proprietary data.
226	>
227	> \(d\) Dissipation of assets or fraudulent transfers that may render a future arbitral award uncollectible.
228	>
229	> • Waiving the right to seek court-ordered provisional relief leaves Whitmore without any remedy during the weeks or months it takes to constitute a tribunal, during which irreparable harm may occur.
230	>
231	> • The emergency arbitrator mechanism provides an additional layer of interim protection but does **not** substitute for court relief. Emergency arbitrator orders may not be enforceable in the same manner as court orders, and not all administering institutions have emergency arbitrator provisions.
232	>
233	> • **Rebecca Stadler has specifically flagged this position as \"non-negotiable\" in client instructions for the current Vantage Specialty Chemicals Inc. transaction.**
234	
235	**[Section 11: Consolidation]{.underline}**
236	
237	**Required:** Consolidation of arbitration proceedings must require the **prior written consent of all parties to all proceedings** proposed to be consolidated. The tribunal must not have unilateral authority to order consolidation, and no single party may compel consolidation over the objection of another party.
238	
239	**Preferred:** Same as Required.
240	
241	**Fallback:** If the counterparty insists on some consolidation mechanism, accept a provision requiring the consent of all claimants and all respondents across all proceedings proposed to be consolidated, plus approval by the applicable tribunal(s).
242	
243	**Rationale:**
244	
245	> • Involuntary consolidation can expose Whitmore (or its fund vehicles) to procedural complexity, delay, and potential prejudice from having unrelated or tangentially related claims merged into a single proceeding.
246	>
247	> • Consolidation should be a consensual process reflecting the agreement of all affected parties.
248	>
249	> • In co-investment contexts, there may be related proceedings involving the target company, lenders (e.g., Claremont National Bank or other senior creditors), minority investors, or other co-investors, and Whitmore must retain control over whether those proceedings are merged with its own.
250	
251	**[Section 12: Joinder of Third Parties]{.underline}**
252	
253	**Required:** Joinder of any third party to the arbitration must require the **consent of all existing parties** to the arbitration **and** the **consent of the third party** to be joined. Both conditions must be satisfied.
254	
255	**NOT ACCEPTABLE:** Joinder at the tribunal\'s discretion without the unanimous consent of all parties. Involuntary joinder undermines party autonomy --- a foundational principle of arbitration --- and may raise due process concerns that jeopardize the enforceability of the award.
256	
257	**Preferred:** Same as Required. Additionally, any joined party must agree in writing to be bound by the arbitration agreement and all procedural orders previously issued by the tribunal.
258	
259	**Fallback:** None --- unanimous consent for joinder is non-negotiable.
260	
261	**Rationale:**
262	
263	> • Arbitration is fundamentally a consensual process. Joining third parties without their consent (or without the consent of existing parties) raises due process concerns and may render the resulting award unenforceable under the Federal Arbitration Act.
264	>
265	> • In the co-investment context, potential third parties could include portfolio company management, lenders, co-investors in other fund vehicles, financial advisors, or other transaction participants. Whitmore must retain control over who participates in the proceeding, what claims are adjudicated, and what information is disclosed to third-party participants.
266	
267	**[Section 13: Damages Limitations]{.underline}**
268	
269	**Required:** The arbitration agreement must include an express **mutual waiver of punitive damages, exemplary damages, and consequential damages** --- including but not limited to lost profits, lost opportunities, diminution in value of other investments, and reputational harm.
270	
271	**Required Carve-Out:** The damages waiver does **not** apply in cases of **fraud** or **willful misconduct**. In such cases, the tribunal may award any damages available under applicable law, including punitive and consequential damages where permitted by the governing law.
272	
273	**Preferred:** The damages limitation should be mutual and should apply to all claims arising under the arbitration agreement and the underlying co-investment agreement, regardless of the legal theory (contract, tort, equity, or otherwise).
274	
275	**Fallback:** If the counterparty resists a full consequential damages waiver, Whitmore will accept a waiver of punitive and exemplary damages only (with the fraud/willful misconduct carve-out preserved). Outside counsel must escalate to the General Counsel before accepting a narrower damages limitation.
276	
277	**Rationale:**
278	
279	> • Uncapped damages exposure --- particularly punitive and consequential damages --- creates disproportionate risk in high-value co-investment transactions. A \$325 million equity investment could theoretically give rise to multi-billion-dollar consequential damages claims based on lost profits, lost deal opportunities, or portfolio-wide impact.
280	>
281	> • The mutual waiver allocates this risk symmetrically and is consistent with market practice in private equity co-investment agreements.
282	>
283	> • The fraud/willful misconduct carve-out preserves accountability for genuinely egregious conduct and ensures that the damages limitation cannot be used as a shield for bad-faith behavior.
284	
285	**[Section 14: Fees and Costs]{.underline}**
286	
287	**Required:** The arbitration agreement must include a **prevailing-party fee-shifting provision** under which the substantially prevailing party is entitled to recover its **reasonable attorneys\' fees, expert witness fees, arbitrator fees, administrative fees, and other costs** of the arbitration from the non-prevailing party.
288	
289	**Preferred:** The tribunal determines which party is the \"substantially prevailing party\" and the reasonableness of claimed fees and costs in the final award.
290	
291	**Fallback:** If the counterparty objects to full fee-shifting, accept a provision granting the tribunal discretion to allocate fees and costs based on the relative success of the parties\' respective claims and defenses.
292	
293	**NOT ACCEPTABLE:** A provision under which each party bears its own attorneys\' fees and costs regardless of outcome. Such a provision incentivizes frivolous claims and tactical arbitration filings because there is no cost consequence for the losing party.
294	
295	**Rationale:**
296	
297	> • Fee-shifting deters frivolous or tactical claims.
298	>
299	> • Fee-shifting ensures the prevailing party is made whole --- or closer to whole --- by recovering the costs of vindicating its rights.
300	>
301	> • Fee-shifting aligns the economic incentives of both parties with the merits of their respective positions, promoting good-faith engagement in the arbitral process.
302	
303	**[Section 15: Statute of Limitations]{.underline}**
304	
305	**Required:** The arbitration agreement must **not** shorten the applicable statute of limitations below the statutory period under the governing substantive law. The contractual limitations period must **track** the statutory period.
306	
307	**Required Minimum:** In no event shall the limitations period for contract-based claims be shorter than **three (3) years** from the date the claim accrues.
308	
309	**Reference:** Under Delaware law (Whitmore\'s preferred governing law), the statute of limitations for breach of contract claims not under seal is **three (3) years** (10 Del. C. § 8106). Under New York law (Whitmore\'s fallback governing law), the statute of limitations for breach of contract claims is **six (6) years** (N.Y. C.P.L.R. § 213).
310	
311	**NOT ACCEPTABLE:** Any contractual shortening of the statute of limitations below the applicable statutory period. Shortened limitations periods may be unenforceable in certain jurisdictions, create traps for the unwary, and may bar legitimate claims before a party has had an adequate opportunity to discover the relevant facts giving rise to the claim.
312	
313	**Preferred:** Silent on limitations --- that is, let the statutory limitations period apply by default under the governing law without any contractual modification.
314	
315	**Fallback:** If the counterparty insists on including a contractual limitations period, it must be no shorter than the longer of (a) the applicable statutory period and (b) three (3) years.
316	
317	**Rationale:**
318	
319	> • Private equity disputes --- particularly those involving valuation, earnout, governance, or fiduciary duty matters --- often do not fully manifest until well after the triggering event. Delayed discovery of breaches is common in contexts involving complex financial reporting, quarterly and annual audit cycles, and multi-year investment horizons.
320	>
321	> • A **one (1) year** limitations period --- commonly proposed by counterparties --- is particularly dangerous because fund operations involve quarterly and annual reporting cycles that may not reveal breaches or losses within twelve (12) months of the triggering event. By the time a breach is identified through the normal course of fund reporting and audit, a one-year limitations period may have already expired.
322	>
323	> • The three-year minimum floor is set at the Delaware statutory period, which is the shortest limitations period applicable under any of Whitmore\'s preferred governing law options.
324	
325	**[Section 16: Class, Collective, and Representative Action Waiver]{.underline}**
326	
327	**Required:** The arbitration agreement must include an **express waiver** of the right to participate in or bring **class actions, collective actions, or representative proceedings** of any kind. All disputes must be arbitrated on an **individual basis** between the named parties to the agreement.
328	
329	**Required Language** (or substantially equivalent):
330	
331	> *\"The parties agree that any arbitration under this Agreement shall be conducted on an individual basis only. No party may bring or participate in any class, collective, consolidated, or representative proceeding in arbitration or in any court. The arbitral tribunal shall have no authority to preside over any form of class, collective, or representative proceeding.\"*
332	
333	**Preferred:** Same as Required.
334	
335	**Fallback:** None --- this is non-negotiable.
336	
337	**Rationale:**
338	
339	> • Class or representative arbitration vastly increases Whitmore\'s exposure and introduces procedural complexity that is inconsistent with the bilateral nature of co-investment agreements.
340	>
341	> • In the private equity co-investment context, the risk is that minority investors, co-investors in parallel vehicles, or other stakeholders could attempt to aggregate claims against Whitmore or a Whitmore-managed fund vehicle.
342	>
343	> • An express waiver eliminates this risk and ensures that each dispute is resolved on its own facts between the parties to the specific agreement.
344	
345	**[Section 17: Expedited Procedures for Critical Disputes]{.underline}**
346	
347	**Required:** The arbitration agreement must include an **expedited dispute resolution track** for disputes involving any of the following subject matters:
348	
349	> 1\. **Capital call disputes** --- including disputes regarding the timing, amount, validity, or enforceability of capital calls.
350	>
351	> 2\. **Drag-along rights** --- including disputes regarding the exercise, conditions, pricing, or procedural requirements of drag-along provisions.
352	>
353	> 3\. **Buy-sell provisions** --- including disputes regarding the triggering, valuation, mechanics, or timing of buy-sell (shotgun) clauses.
354	
355	**Required Expedited Procedure Terms:**
356	
357	> • **Sole arbitrator** (notwithstanding the three-member panel requirement for general disputes under Section 4).
358	>
359	> • **Arbitrator appointment within ten (10) business days** of the filing of the demand for arbitration.
360	>
361	> • **Hearing to be conducted within thirty (30) days** of the arbitrator\'s appointment.
362	>
363	> • **Final award to be rendered within forty-five (45) days** of the filing of the demand for arbitration.
364	>
365	> • **Limited discovery:** Document production only (no depositions); maximum of five (5) document requests per side.
366	
367	**Preferred:** Same as Required.
368	
369	**Fallback:** If the counterparty objects to the 45-day timeline, accept up to **sixty (60) days**, but not longer.
370	
371	**Rationale:**
372	
373	> • Capital call, drag-along, and buy-sell disputes have time-sensitive commercial consequences that cannot tolerate standard arbitration timelines.
374	>
375	> • A delayed or disputed capital call can jeopardize a transaction closing or trigger default provisions under the fund\'s limited partnership agreement.
376	>
377	> • A disputed drag-along can prevent or delay a sale transaction, causing the window for an exit to close.
378	>
379	> • A buy-sell dispute can freeze governance and create operational paralysis within the portfolio company.
380	>
381	> • Standard arbitration timelines (90+ days to hearing, plus additional time for post-hearing briefing and award) are inadequate for these time-critical contexts.
382	>
383	> • **Rebecca Stadler has specifically identified expedited procedures for capital call and drag-along disputes as \"critical for fund governance\" in the current Vantage Specialty Chemicals Inc. transaction.**
384	
385	**[Section 18: Arbitral Award --- Timeline and Content]{.underline}**
386	
387	**Required:** The arbitral tribunal must issue its final award within **ninety (90) days** of the close of proceedings --- defined as the date on which the last post-hearing submission is filed or the hearing transcript is received by the tribunal, whichever is later.
388	
389	**Required:** The award must include both of the following:
390	
391	> 1\. **Findings of fact** --- a detailed statement of the factual determinations underlying the award.
392	>
393	> 2\. **Conclusions of law** --- a detailed statement of the legal analysis and reasoning applied to those facts.
394	
395	A \"reasoned award\" that does not include both specific findings of fact and specific conclusions of law is insufficient to satisfy this requirement.
396	
397	**Preferred:** Same as Required.
398	
399	**Fallback:** If the counterparty objects to the 90-day timeline, accept up to **one hundred twenty (120) days**, but findings of fact and conclusions of law are **non-negotiable** and must be included regardless of timeline.
400	
401	**Rationale:**
402	
403	> • A 90-day timeline is consistent with market practice for commercial arbitration of this complexity and provides the tribunal adequate time to deliberate and draft a thorough award.
404	>
405	> • Findings of fact and conclusions of law are necessary to: (a) enable meaningful review of the award, including for manifest disregard of the law under the Federal Arbitration Act; (b) provide a sufficient record for any appellate arbitration (*see* Section 19); and (c) ensure the tribunal has rigorously analyzed the dispute rather than issuing a summary disposition.
406	
407	**[Section 19: Appellate Arbitration]{.underline}**
408	
409	**Required:** For any award (or series of awards in a single proceeding) that exceeds **\$25 million** in aggregate monetary relief --- including damages, interest, fees, and costs --- the arbitration agreement must provide for **optional appellate arbitration**.
410	
411	**Required Mechanism:** The appellate arbitration shall be conducted under the **AAA Optional Appellate Arbitration Rules** or, if the administering institution is JAMS, the JAMS equivalent appellate rules.
412	
413	**Required Terms:**
414	
415	> • Either party may elect to appeal the award by filing a notice of appeal within **thirty (30) days** of the issuance of the award.
416	>
417	> • The appellate panel shall consist of **three (3) arbitrators** drawn from the administering institution\'s appellate roster.
418	>
419	> • The standard of review shall be as set forth in the applicable appellate arbitration rules (generally, errors of law that are material and prejudicial, and findings of fact that are clearly erroneous).
420	>
421	> • The award shall not become final and enforceable until the appeal period has expired without a notice of appeal being filed, or the appellate panel has issued its decision on the appeal.
422	
423	**Preferred:** Same as Required.
424	
425	**Fallback:** If the counterparty objects to mandatory appellate arbitration provisions, accept a provision that the parties may agree post-award to submit the award to appellate arbitration by mutual written consent.
426	
427	**Rationale:**
428	
429	> • A \$25 million or greater award in a co-investment dispute could have fund-level implications, including material effects on fund returns, reserves, and LP distributions.
430	>
431	> • The finality of arbitration, while generally an advantage, creates unacceptable risk at this magnitude without a check against material legal error.
432	>
433	> • The AAA Optional Appellate Arbitration Rules provide a structured, efficient review mechanism that preserves the efficiency benefits of arbitration while protecting against erroneous awards of significant magnitude.
434	
435	**[Section 20: Document Retention]{.underline}**
436	
437	**Required:** The arbitration agreement must **NOT** require the destruction of documents or materials produced during the arbitration. Any mandatory destruction clause must be **deleted** from the counterparty\'s proposed agreement.
438	
439	**Required:** All documents, materials, submissions, transcripts, evidence, and awards from the arbitration must be **retained for a minimum of seven (7) years** following the issuance of the final award (or the final appellate award, if appellate arbitration is invoked under Section 19).
440	
441	**NOT ACCEPTABLE:** Any provision requiring destruction of arbitration documents within any time period after the issuance of the award. This is a categorical prohibition. Provisions requiring destruction within 30, 60, 90, or any other number of days are equally unacceptable.
442	
443	**Rationale:**
444	
445	> • Whitmore\'s fund document retention policies require a minimum seven (7) year retention period for all material fund records, including dispute-related records.
446	>
447	> • Premature destruction may compromise the ability to enforce or defend against vacatur of the award in subsequent court proceedings.
448	>
449	> • Premature destruction may compromise appellate arbitration rights under Section 19 if the relevant materials are no longer available.
450	>
451	> • Tax and regulatory audit cycles may require access to arbitration records for years after the issuance of the award.
452	>
453	> • LP reporting obligations and fiduciary duties may require reference to arbitration records during the life of the fund and any applicable wind-down period.
454	
455	**Preferred:** Same as Required.
456	
457	**Fallback:** If the counterparty insists on some document management provision, accept a provision requiring the **return** (not destruction) of produced documents to the producing party, with retention of all other materials --- including submissions, transcripts, orders, and awards --- for a minimum of seven (7) years.
458	
459	**[Section 21: Language of Arbitration]{.underline}**
460	
461	**Required:** The language of the arbitration must be **English** for all domestic U.S. transactions. This is standard and non-controversial.
462	
463	**[Section 22: General Negotiation Instructions]{.underline}**
464	
465	Outside counsel must review every counterparty-proposed arbitration agreement against each section of this playbook. The following priority classifications govern the order and intensity of negotiation:
466	
467	**Critical (Non-Negotiable):**
468	
469	> • Preservation of interim and emergency court relief (Section 10)
470	>
471	> • Arbitrator panel composition for disputes over \$10M (Section 4)
472	>
473	> • Governing law --- Delaware or New York only (Section 6)
474	>
475	> • Statute of limitations --- no shortening below statutory period / 3-year minimum (Section 15)
476	>
477	> • Class, collective, and representative action waiver (Section 16)
478	
479	**Important (Strongly Preferred):**
480	
481	> • Administering institution --- AAA, not ICC for domestic transactions (Section 2)
482	>
483	> • Seat of arbitration --- Atlanta, or New York as fallback (Section 3)
484	>
485	> • Confidentiality provision --- must be present and comprehensive (Section 9)
486	>
487	> • Damages limitation --- waiver of punitive and consequential damages (Section 13)
488	>
489	> • Fee-shifting --- prevailing-party recovery (Section 14)
490	>
491	> • Joinder and consolidation --- unanimous consent required (Sections 11--12)
492	>
493	> • Document retention --- no destruction, 7-year minimum retention (Section 20)
494	>
495	> • Appellate arbitration mechanism for awards over \$25M (Section 19)
496	
497	**Recommended:**
498	
499	> • Arbitrator qualifications --- 15 years PE/M&A experience (Section 5)
500	>
501	> • Discovery limitations --- specific caps on depositions, document requests, experts (Section 8)
502	>
503	> • Award timeline and content --- 90 days, findings of fact and conclusions of law (Section 18)
504	>
505	> • Expedited procedures for capital call, drag-along, and buy-sell disputes (Section 17)
506	
507	**Markup Protocol:** If a counterparty\'s proposed agreement departs from a \"Required\" position, outside counsel must flag the departure in the redline markup with a comment referencing the specific playbook section number and indicating the position classification (Required, Preferred, or Fallback).
508	
509	**Escalation Protocol:** If the counterparty is unwilling to accept a Required position after good-faith negotiation, outside counsel must escalate to the General Counsel (Rebecca Stadler) before conceding or accepting any compromise.
510	
511	**Current Transaction Note:** For the current Vantage Specialty Chemicals Inc. / Cascadian Growth Fund LP co-investment, the markup deadline is **January 13, 2025**. All markup submissions must be strictly on time.
512	
513	**[Section 23: Approved Sample Language]{.underline}**
514	
515	Whitmore maintains a library of approved sample arbitration clauses, available upon request from the General Counsel\'s office. Outside counsel should use the sample language as a starting point for any new drafting and should reference the sample clauses when inserting provisions that are absent from a counterparty\'s proposed agreement.
516	
517	The following provisions may need to be drafted and inserted from scratch if they are absent from the counterparty\'s form:
518	
519	> • Confidentiality provision (Section 9)
520	>
521	> • Damages limitation and waiver (Section 13)
522	>
523	> • Class, collective, and representative action waiver (Section 16)
524	>
525	> • Expedited procedures for capital call, drag-along, and buy-sell disputes (Section 17)
526	>
527	> • Appellate arbitration mechanism (Section 19)
528	
529	Outside counsel should contact the General Counsel\'s office to obtain the current approved forms of these provisions.
530	
531	**[Section 24: Version History and Contact Information]{.underline}**
532	
533	**Version History:**
534	
535	  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
536	  **Version**             **Date**                **Description**
537	  ----------------------- ----------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
538	  3.0                     November 15, 2024       Current version. Added appellate arbitration section (Section 19), expedited procedures section (Section 17), and revised arbitrator qualification requirements (Section 5). Updated negotiation priority classifications.
539	
540	  2.0                     March 2022              Initial comprehensive update.
541	
542	  1.0                     September 2019          Original version.
543	  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
544	
545	**Contact:**
546	
547	Rebecca Stadler, General Counsel Whitmore Capital Partners LLC 3400 Peachtree Road NE, Suite 1200 Atlanta, GA 30326
548	
549	**Distribution Notice:** This playbook is distributed on a confidential basis to approved outside counsel firms only. It is protected by the attorney-client privilege and the work product doctrine. Current distribution list includes Hargrove, Wynn & Calloway LLP (David Ostrander, Partner; Priya Nakamura, Associate). Do not copy or distribute without the prior written consent of the General Counsel.
550	
551	**END OF DOCUMENT** PRIVILEGED & CONFIDENTIAL --- ATTORNEY-CLIENT PRIVILEGED / WORK PRODUCT
552	
[ASSISTANT] The playbook is detailed and most of the proposed form departs from it. Before drafting, I'll check the tooling and the original .docx XML so the redline can use real tracked changes on the original file.
[ACTION] Bash {"command": "cd /tmp; python3 -c \"import docx, sys; print('python-docx', docx.__version__ if hasattr(docx,'__version__') else 'ok')\" 2>&1; pandoc --version | head -1; mkdir -p /tmp/orig && cd /tmp/orig && python3 -I -c \"import zipfile;z=zipfile.ZipFile('./documents/proposed-arbitration-agreement.docx');print(z.namelist());z.extractall('.')\"; wc -c word/document.xml; head -c 3000 word/document.xml", "description": "Check python-docx, pandoc, and unpack original docx XML"}
[OBSERVATION]
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import docx, sys; print('python-docx', docx.__version__ if hasattr(docx,'__version__') else 'ok')
    ^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'docx'
pandoc 3.12.1
['[Content_Types].xml', '_rels/.rels', 'docProps/core.xml', 'docProps/app.xml', 'word/document.xml', 'word/_rels/document.xml.rels', 'word/styles.xml', 'word/stylesWithEffects.xml', 'word/settings.xml', 'word/webSettings.xml', 'word/fontTable.xml', 'word/theme/theme1.xml', 'customXml/item1.xml', 'customXml/_rels/item1.xml.rels', 'customXml/itemProps1.xml', 'word/numbering.xml', 'word/footer1.xml', 'word/header1.xml', 'docProps/thumbnail.jpeg']
   61226 word/document.xml
<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" xmlns:mo="http://schemas.microsoft.com/office/mac/office/2008/main" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:mv="urn:schemas-microsoft-com:mac:vml" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" mc:Ignorable="w14 wp14"><w:body><w:p><w:pPr><w:spacing w:line="276" w:lineRule="auto" w:before="0" w:after="120"/><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>EXHIBIT F TO CO-INVESTMENT AGREEMENT</w:t></w:r></w:p><w:p><w:pPr><w:spacing w:line="276" w:lineRule="auto" w:before="0" w:after="120"/><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>ARBITRATION AGREEMENT</w:t></w:r></w:p><w:p><w:pPr><w:spacing w:line="276" w:lineRule="auto" w:before="0" w:after="120"/><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>Dated as of January 15, 2025</w:t></w:r></w:p><w:p><w:pPr><w:spacing w:line="276" w:lineRule="auto" w:before="0" w:after="120"/><w:jc w:val="both"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>This Arbitration Agreement (this "</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>Agreement</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>") is entered into as of January 15, 2025, by and between the following parties in connection with that certain Co-Investment Agreement dated as of even date herewith (the "</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:color w:val="000000"/><w:sz w
Shell cwd was reset to .
[ASSISTANT] python-docx isn't installed, so I'll build the redline by writing WordprocessingML directly: keep the original package and header/footer, and emit `w:ins`/`w:del` runs. First I'll index the original paragraphs so the revised text can be aligned to them.
[ACTION] Bash {"command": "mkdir -p /tmp/build && cat > /tmp/build/extract.py <<'EOF'\nimport xml.etree.ElementTree as ET, json, sys\nW = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'\nroot = ET.parse('/tmp/orig/word/document.xml').getroot()\nbody = root.find(W+'body')\nparas = []\nfor p in body.iter(W+'p'):\n    segs = []\n    for r in p.iter(W+'r'):\n        rpr = r.find(W+'rPr')\n        b = rpr is not None and rpr.find(W+'b') is not None\n        u = rpr is not None and rpr.find(W+'u') is not None\n        i = rpr is not None and rpr.find(W+'i') is not None\n        t = ''.join((x.text or '') for x in r.iter(W+'t'))\n        if t: segs.append((t, b, u, i))\n    text = ''.join(s[0] for s in segs)\n    paras.append({'segs': segs, 'text': text})\njson.dump(paras, open('/tmp/build/orig_paras.json','w'))\nfor idx, p in enumerate(paras):\n    if p['text'].strip():\n        print(idx, p['text'][:90])\nEOF\npython3 -I /tmp/build/extract.py; echo; python3 -I -c \"\nimport xml.etree.ElementTree as ET\nW='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'\nr=ET.parse('/tmp/orig/word/document.xml').getroot().find(W+'body')\nprint([c.tag.split('}')[1] for c in r][-3:])\nprint(ET.tostring(r[-1]).decode()[:600])\"", "description": "Index original document paragraphs with ids"}
[OBSERVATION]
0 EXHIBIT F TO CO-INVESTMENT AGREEMENT
1 ARBITRATION AGREEMENT
2 Dated as of January 15, 2025
3 This Arbitration Agreement (this "Agreement") is entered into as of January 15, 2025, by a
4 RECITALS
5 WHEREAS, Whitmore Capital Fund III LP, a Delaware limited partnership ("Whitmore"), an inv
6 WHEREAS, pursuant to the Co-Investment Agreement, the Parties have agreed to jointly acqui
7 WHEREAS, the Co-Investment Agreement governs, among other things, governance rights, drag-
8 WHEREAS, the Parties desire to establish the terms and procedures by which disputes arisin
9 NOW, THEREFORE, in consideration of the mutual covenants and agreements set forth in the C
11 ARTICLE I — DEFINITIONS
12 As used in this Agreement, the following terms shall have the meanings set forth below:
13 "Agreement" means this Arbitration Agreement, as it may be amended from time to time in ac
14 "Arbitral Tribunal" or "Tribunal" means the arbitrator or arbitrators appointed pursuant t
15 "Award" means any interim, partial, or final award rendered by the Arbitral Tribunal in co
16 "Claimant" means the Party initiating a Proceeding by filing a request for arbitration.
17 "Co-Investment Agreement" or "CIA" has the meaning set forth in the Recitals.
18 "Company" means Vantage Specialty Chemicals Inc., a Delaware corporation.
19 "Dispute" means any dispute, controversy, or claim arising out of, relating to, or in conn
20 "ICC" means the International Chamber of Commerce.
21 "ICC Rules" means the Rules of Arbitration of the International Chamber of Commerce in eff
22 "Party" and "Parties" have the meanings set forth in the Recitals.
23 "Proceedings" means any arbitration proceedings commenced pursuant to this Agreement.
24 "Respondent" means the Party against whom a request for arbitration is filed.
25 "Seat" means Seattle, Washington, which shall be the juridical seat of any arbitration con
26 ARTICLE II — AGREEMENT TO ARBITRATE; SCOPE
27 Section 2.1 — Agreement to Arbitrate. Any and all disputes, controversies, or claims arisi
28 Section 2.2 — Exclusive Remedy. Arbitration under this Agreement shall be the exclusive re
29 ARTICLE III — SEAT, LANGUAGE, AND GOVERNING LAW
30 Section 3.1 — Seat of Arbitration. The seat (legal place) of arbitration shall be Seattle,
31 Section 3.2 — Language. The language of the arbitration shall be English. All submissions,
32 Section 3.3 — Governing Law. This Agreement shall be governed by and construed in accordan
34 ARTICLE IV — ARBITRATOR APPOINTMENT AND QUALIFICATIONS
35 Section 4.1 — Number of Arbitrators. The arbitration shall be conducted by a sole arbitrat
36 Section 4.2 — Appointment Procedure. The Parties shall endeavor to agree upon a mutually a
37 Section 4.3 — Qualifications. The Arbitrator shall be a neutral individual independent of 
38 ARTICLE V — ARBITRATION PROCEDURES
39 Section 5.1 — Discovery. Discovery shall be conducted in accordance with the ICC Rules, wi
40 Section 5.2 — Hearings. The Arbitrator shall hold hearings as the Arbitrator deems necessa
41 Section 5.3 — Evidence. The Arbitrator shall have the authority to receive and consider su
42 ARTICLE VI — INTERIM AND EMERGENCY RELIEF
43 Section 6.1 — Waiver of Court Relief. The Parties hereby expressly waive any right to seek
45 ARTICLE VII — CONSOLIDATION AND JOINDER
46 Section 7.1 — Consolidation. The Tribunal may, at the request of either Party, consolidate
47 Section 7.2 — Joinder of Third Parties. Third parties may be joined to the arbitration at 
48 ARTICLE VIII — AWARD
49 Section 8.1 — Timing and Form of Award. The Arbitrator shall use best efforts to issue a r
50 Section 8.2 — Finality. The award of the Arbitrator shall be final and binding upon the Pa
51 Section 8.3 — Remedies. The Arbitrator shall have the authority to award any remedy or rel
53 ARTICLE IX — COSTS AND FEES
54 Section 9.1 — Allocation of Costs. Each Party shall bear its own costs and expenses of the
55 Section 9.2 — Administrative Costs. The administrative fees and expenses of the ICC and th
56 ARTICLE X — LIMITATIONS PERIOD
57 Section 10.1 — Statute of Limitations. All claims subject to arbitration under this Agreem
58 ARTICLE XI — DOCUMENT RETENTION AND DESTRUCTION
59 Section 11.1 — Post-Arbitration Document Handling. The Parties agree that, within thirty (
61 ARTICLE XII — GENERAL PROVISIONS
62 Section 12.1 — Notices. All notices, requests, demands, and other communications under thi
63 Section 12.2 — Entire Agreement. This Agreement constitutes the entire agreement between t
64 Section 12.3 — Amendment and Waiver. This Agreement may not be amended, modified, or suppl
65 Section 12.4 — Severability. If any provision of this Agreement is held to be invalid, ill
66 Section 12.5 — Counterparts. This Agreement may be executed in counterparts, each of which
67 Section 12.6 — Relationship to Co-Investment Agreement. This Agreement is Exhibit F to and
68 Section 12.7 — Survival. This Agreement shall survive the termination or expiration of the
70 [Signature Page Follows]
72 IN WITNESS WHEREOF, the Parties have executed this Arbitration Agreement as of the date fi
73 WHITMORE CAPITAL FUND III LP
74 By: Whitmore Capital Partners LLC, its General Partner
75 By: ________
76 Name: ________
77 Title: ________
78 Date: ________
79 CASCADIAN GROWTH FUND LP
80 By: Cascadian Growth Management LLC, its General Partner
81 By: ________
82 Name: ________
83 Title: ________
84 Date: ________

['p', 'p', 'sectPr']
<ns0:sectPr xmlns:ns0="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:ns1="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ns0:rsidR="00FC693F" ns0:rsidRPr="0006063C" ns0:rsidSect="00034616"><ns0:footerReference ns0:type="default" ns1:id="rId9" /><ns0:headerReference ns0:type="default" ns1:id="rId10" /><ns0:pgSz ns0:w="12240" ns0:h="15840" /><ns0:pgMar ns0:top="1440" ns0:right="1800" ns0:bottom="1440" ns0:left="1800" ns0:header="720" ns0:footer="720" ns0:gutter="0" /><ns0:cols ns0:space="720" /><ns0:docGrid ns0:linePitch="360" /></ns0:sectPr>
[ASSISTANT] I have what I need. The proposed form departs from the playbook on nearly every topic, and I found some issues to raise with the GC. Before drafting, I'm checking two of them against the text: the playbook's expedited deadlines, and whether the playbook's confidentiality exceptions conflict with its own LP-reporting rationale.
[ACTION] Bash {"command": "python3 -I -c \"\n# Expedited track timing per playbook s.17: appointment <=10 business days (~14 calendar), hearing <=30 days after appointment, award <=45 days after demand\nappt_max_cal = 14   # 10 business days, roughly 14 calendar days\nhearing_latest = appt_max_cal + 30\nprint('latest hearing day after filing:', hearing_latest, '| award deadline day:', 45, '| days left for post-hearing + award:', 45-hearing_latest)\n\"; grep -n \"LP reporting\\|LP distributions\\|LP-reporting\" /tmp/playbook.txt | head", "description": "Check expedited timeline feasibility and LP-reporting references"}
[OBSERVATION]
latest hearing day after filing: 44 | award deadline day: 45 | days left for post-hearing + award: 1
429:> • A \$25 million or greater award in a co-investment dispute could have fund-level implications, including material effects on fund returns, reserves, and LP distributions.
453:> • LP reporting obligations and fiduciary duties may require reference to arbitration records during the life of the fund and any applicable wind-down period.
[ASSISTANT] Confirmed: the playbook's expedited sub-deadlines leave one day between the latest permissible hearing and the 45-day award. I'll draft to the playbook terms with a bracketed placeholder and flag it. Now I'm writing the redline builder, which emits real tracked changes into the original package.
[ACTION] Bash {"command": "cat > /tmp/build/build_redline.py <<'PYEOF'\nimport json, re, difflib, zipfile, xml.etree.ElementTree as ET\nfrom xml.sax.saxutils import escape\n\nSRC = './documents/proposed-arbitration-agreement.docx'\nOUT = './output/redlined-arbitration-agreement.docx'\nAUTH = escape('Hargrove, Wynn & Calloway LLP')\nW = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'\nNOTE_COLOR = '1F4E79'\n\n# ---------- original paragraphs as (char, bold, underline, italic) ----------\nroot = ET.parse('/tmp/orig/word/document.xml').getroot()\nORIG_P = list(root.find(W+'body').iter(W+'p'))\nORIG_CHARS, ORIG_JC = [], []\nfor p in ORIG_P:\n    chars = []\n    for r in p.iter(W+'r'):\n        rpr = r.find(W+'rPr')\n        f = lambda t: rpr is not None and rpr.find(W+t) is not None\n        for t in r.iter(W+'t'):\n            for c in (t.text or ''):\n                chars.append((c, f('b'), f('u'), f('i')))\n    ORIG_CHARS.append(chars)\n    ppr = p.find(W+'pPr')\n    jc = ppr.find(W+'jc') if ppr is not None else None\n    ORIG_JC.append(jc.get(W+'val') if jc is not None else 'both')\n\ndef parse_markup(s):\n    \"\"\"**bold** and __u
[OBSERVATION]
wrote ./output/redlined-arbitration-agreement.docx revisions: 14751
Shell cwd was reset to .
[ASSISTANT] The build wrote, but 14,751 revision IDs is far more than the edits should need. I'll inspect the output for runaway fragmentation before trusting it.
[ACTION] Bash {"command": "cd /tmp/build && rm -rf chk && mkdir chk && python3 -I -c \"\nimport zipfile,re\nx=zipfile.ZipFile('./output/redlined-arbitration-agreement.docx').read('word/document.xml').decode()\nprint('ins',x.count('<w:ins '),'del',x.count('<w:del '),'paras',x.count('<w:p>'))\nprint('paragraph-level changes sample:', len(x))\n\" ; python3 -I -c \"\nimport zipfile\nprint(zipfile.ZipFile('./output/redlined-arbitration-agreement.docx').namelist()[:3])\"; pandoc './output/redlined-arbitration-agreement.docx' -t plain --wrap=none --track-changes=accept -o /tmp/build/accepted.txt && pandoc './output/redlined-arbitration-agreement.docx' -t plain --wrap=none --track-changes=reject -o /tmp/build/rejected.txt && wc -l /tmp/build/accepted.txt /tmp/build/rejected.txt && head -c 1500 /tmp/build/rejected.txt",
[OBSERVATION]
ins 13861 del 890 paras 119
paragraph-level changes sample: 5065553
['[Content_Types].xml', '_rels/.rels', 'docProps/core.xml']
     219 /tmp/build/accepted.txt
     155 /tmp/build/rejected.txt
     374 total
EXHIBIT F TO CO-INVESTMENT AGREEMENT

ARBITRATION AGREEMENT

Dated as of January 15, 2025

This Arbitration Agreement (this "Agreement") is entered into as of January 15, 2025, by and between the following parties in connection with that certain Co-Investment Agreement dated as of even date herewith (the "Co-Investment Agreement"). Capitalized terms used but not otherwise defined herein shall have the meanings ascribed to them in the Co-Investment Agreement.

RECITALS

WHEREAS, Whitmore Capital Fund III LP, a Delaware limited partnership ("Whitmore"), an investment vehicle managed by Whitmore Capital Partners LLC, a Delaware limited liability company, with its principal office at 3400 Peachtree Road NE, Suite 1200, Atlanta, GA 30326, and Cascadian Growth Fund LP, a Delaware limited partnership ("Cascadian"), managed by its general partner, Cascadian Growth Management LLC, a Delaware limited liability company, with its principal office at 1501 Fourth Avenue, Suite 3700, Seattle, WA 98101 (each, a "Party" and together, the "Parties"), have entered into that certain Co-Investment Agreement dated as of January 15, 2025 (the "Co-Investment Agreement");

WHEREAS, pursuant to the Co-Investment Agreement, the Parties have agreed to jointly acquire a controlling interest (approximately 72%) of Vantage Specialty Chemicals Inc., a Delaware corporation headquartered at 10200 Bellaire Boulevard, Suite 400, Houston, TX 77072 (the "Target" or the "Company"), at a total enterprise value of $
Shell cwd was reset to .
[ASSISTANT] The fragmentation is a bug in my grouping code: I compared a list slice to a tuple, so every character became its own run. Fixing both comparisons and rebuilding.
[ACTION] Bash {"command": "cd /tmp/build && python3 -I - <<'EOF'\nimport re\ns = open('build_redline.py', encoding='utf-8').read()\ns = s.replace(\"if out and out[-1][1:] == (b, u, i): out[-1][0] += c\",\n              \"if out and tuple(out[-1][1:]) == (b, u, i): out[-1][0] += c\")\ns = s.replace(\"if segs and segs[-1][0] == kind and segs[-1][2:] == (b, u, i): segs[-1][1] += txt\",\n              \"if segs and segs[-1][0] == kind and tuple(segs[-1][2:]) == (b, u, i): segs[-1][1] += txt\")\nopen('build_redline.py', 'w', encoding='utf-8').write(s)\nEOF\npython3 -I build_redline.py && python3 -I -c \"\nimport zipfile\nx=zipfile.ZipFile('./output/redlined-arbitration-agreement.docx').read('word/document.xml').decode()\nprint('ins',x.count('<w:ins '),'del',x.count('<w:del '))\"; OUT=./output/redlined-arbitration-agreement.docx; pandoc \"$OUT\" -t plain --wrap=none --track-changes=reject -o /tmp/build/rejected.txt; pandoc \"$OUT\" -t plain --wrap=none --track-changes=accept -o /tmp/build/accepted.txt; wc -l /tmp/build/rejected.txt /tmp/build/accepted.txt", "description": "Fix run grouping bug, rebuild, and recount revisions"}
[OBSERVATION]
wrote ./output/redlined-arbitration-agreement.docx revisions: 452
ins 264 del 188
     155 /tmp/build/rejected.txt
     219 /tmp/build/accepted.txt
     374 total
Shell cwd was reset to .
[ASSISTANT] Revision counts look sane now. The key check is that rejecting all changes returns the original text exactly, and accepting them yields the intended revised text.
[ACTION] Bash {"command": "cd /tmp/build && pandoc <runs>/exec/lab-cc-agg1/arbitration-international-dispute-resolution/draft-markup-of-arbitration-agreement/base1/documents/proposed-arbitration-agreement.docx -t plain --wrap=none -o orig_plain.txt 2>/dev/null || pandoc ./documents/proposed-arbitration-agreement.docx -t plain --wrap=none -o orig_plain.txt; diff <(sed 's/[[:space:]]*$//' orig_plain.txt | grep -v '^$') <(sed 's/[[:space:]]*$//' rejected.txt | grep -v '^$') && echo \"REJECT-ALL == ORIGINAL (text)\"; grep -c \"WHITMORE NOTE\" accepted.txt; sed -n '1,4p' accepted.txt | cut -c1-200", "description": "Verify reject-all reproduces original text exactly"}
[OBSERVATION]
REJECT-ALL == ORIGINAL (text)
25
[INTERNAL DRAFT — PRIVILEGED & CONFIDENTIAL — ATTORNEY WORK PRODUCT. Bracketed WHITMORE NOTES reflect the privileged Whitmore Arbitration Playbook (v3.0, Nov. 15, 2024) and fallback positions. Remove 

EXHIBIT F TO CO-INVESTMENT AGREEMENT
Shell cwd was reset to .
[ASSISTANT] Reject-all reproduces the original exactly. Next I'll read the accepted view of the operative sections to check the revised language reads correctly.
[ACTION] Bash {"command": "cd /tmp/build && grep -v \"WHITMORE NOTE\" accepted.txt | grep -v '^$' | sed -n '20,200p' | cut -c1-260", "description": "Review accepted revised text excluding internal notes"}
[OBSERVATION]
"Company" means Vantage Specialty Chemicals Inc., a Delaware corporation.
"Dispute" means any dispute, controversy, or claim arising out of, relating to, or in connection with this Agreement or the Co-Investment Agreement, including any question regarding the existence, formation, validity, interpretation, performance, breach, or te
"Expedited Dispute" has the meaning set forth in Section 5.5.
"Party" and "Parties" have the meanings set forth in the Recitals.
"Proceedings" means any arbitration proceedings commenced pursuant to this Agreement.
"Respondent" means the Party against whom a request for arbitration is filed.
"Seat" means Atlanta, Georgia, which shall be the juridical seat of any arbitration conducted under this Agreement.
ARTICLE II — AGREEMENT TO ARBITRATE; SCOPE
Section 2.1 — Agreement to Arbitrate. Any and all disputes, controversies, or claims arising out of, relating to, or in connection with this Agreement or the Co-Investment Agreement, including but not limited to the formation, validity, interpretation, perform
Section 2.2 — Exclusive Remedy. Arbitration under this Agreement shall be the exclusive remedy for any Dispute, and no Party shall institute any action or proceeding in any court with respect to any Dispute, except (a) as provided in Article VI and (b) as othe
ARTICLE III — SEAT, LANGUAGE, AND GOVERNING LAW
Section 3.1 — Seat of Arbitration. The seat (legal place) of arbitration shall be Atlanta, Georgia. Any hearings shall be conducted at the Seat unless otherwise agreed by the Parties or ordered by the Arbitral Tribunal.
Section 3.2 — Language. The language of the arbitration shall be English. All submissions, correspondence, evidence, and hearings shall be conducted in English.
Section 3.3 — Governing Law. This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to its conflict of laws principles.
ARTICLE IV — ARBITRATOR APPOINTMENT AND QUALIFICATIONS
Section 4.1 — Number of Arbitrators. The arbitration shall be conducted by a three (3)-member Tribunal, each member of which shall be an "Arbitrator" appointed in accordance with Section 4.2, except that an Expedited Dispute shall be conducted by a sole Arbitr
Section 4.2 — Appointment Procedure. (a) Each Party shall appoint one (1) Arbitrator within thirty (30) days following the filing of the request for arbitration; where multiple Parties are aligned as claimant or respondent, those Parties shall jointly appoint 
Section 4.3 — Qualifications. Each Arbitrator (including any sole Arbitrator) shall be a neutral individual independent of the Parties and shall: (a) have at least fifteen (15) years of professional experience in private equity, mergers and acquisitions, or co
ARTICLE V — ARBITRATION PROCEDURES
Section 5.1 — Discovery. Except as provided in Section 5.5 with respect to Expedited Disputes, discovery shall be conducted in accordance with the AAA Rules, subject to the following limits: (a) each Party may take up to three (3) fact depositions, each not to
Section 5.2 — Hearings. The Tribunal shall hold hearings as the Tribunal deems necessary and appropriate. Hearings shall be held at the Seat unless otherwise agreed by the Parties or directed by the Arbitrator.
Section 5.3 — Evidence. The Tribunal shall have the authority to receive and consider such evidence as the Arbitrator deems relevant and material, including documentary evidence, witness testimony, and expert reports. The Tribunal shall determine the admissibi
Section 5.4 — Confidentiality. The existence of any Proceeding, all submissions, briefs, motions, and pleadings filed in any Proceeding, all evidence, testimony, exhibits, and documents produced or presented in any Proceeding, all orders, rulings, and awards i
Section 5.5 — Expedited Disputes. Notwithstanding Sections 4.1, 5.1, and 8.1, the following shall apply to any Dispute concerning (i) the timing, amount, validity, or enforceability of a capital call, (ii) the exercise, conditions, pricing, or procedural requi
ARTICLE VI — INTERIM AND EMERGENCY RELIEF
Section 6.1 — Preservation of Court Interim Relief. Nothing in this Agreement shall preclude or restrict any Party from seeking provisional, interim, or injunctive measures, including temporary restraining orders, preliminary injunctions, attachments, and othe
Section 6.2 — Emergency Arbitrator. Any Party may apply for emergency measures of protection under the AAA Optional Rules for Emergency Measures of Protection in effect at the time of the application. Any order of an emergency arbitrator shall be binding on th
ARTICLE VII — CONSOLIDATION AND JOINDER
Section 7.1 — Consolidation. No Proceeding shall be consolidated with any other arbitration or proceeding without the prior written consent of all Parties to all Proceedings proposed to be consolidated. The Tribunal shall have no authority to order consolidati
Section 7.2 — Joinder of Third Parties. No third party may be joined to any Proceeding without (a) the prior written consent of all Parties to such Proceeding and (b) the prior written consent of the third party to be joined. Any joined party shall agree in wr
Section 7.3 — Individual Proceedings. The Parties agree that any arbitration under this Agreement shall be conducted on an individual basis only. No Party may bring or participate in any class, collective, or representative proceeding in arbitration or in any 
ARTICLE VIII — AWARD
Section 8.1 — Timing and Form of Award. The Tribunal shall issue its final award within ninety (90) days after the close of Proceedings, which for this purpose shall be the later of the date on which the last post-hearing submission is filed and the date on wh
Section 8.2 — Finality. Subject to Section 8.5, the award of the Tribunal shall be final and binding upon the Parties and shall not be subject to appeal, except as otherwise provided by applicable law. Judgment upon the award may be entered in any court of com
Section 8.3 — Remedies. The Tribunal shall have the authority to award any remedy or relief that a court of competent jurisdiction could grant, including but not limited to specific performance, injunctive relief, and monetary damages, in each case subject to 
Section 8.4 — Mutual Waiver of Certain Damages. To the fullest extent permitted by law, each Party waives, and the Tribunal shall not award, any punitive damages, exemplary damages, or consequential damages arising under or in connection with this Agreement or
Section 8.5 — Optional Appellate Arbitration. If an award (or series of awards in a single Proceeding) exceeds Twenty-Five Million Dollars ($25,000,000) in aggregate monetary relief, including damages, interest, fees, and costs, either Party may elect to appea
ARTICLE IX — COSTS AND FEES
Section 9.1 — Allocation of Costs. The substantially prevailing Party shall be entitled to recover from the non-prevailing Party its reasonable attorneys' fees, expert witness fees, Arbitrator fees, administrative fees, and other costs of the arbitration. The 
Section 9.2 — Administrative Costs. The administrative fees and expenses of the AAA and the fees and expenses of the Arbitrators shall be shared equally by the Parties, subject to reallocation in the award under Section 9.1.
ARTICLE X — LIMITATIONS PERIOD
Section 10.1 — Statute of Limitations. Claims subject to arbitration under this Agreement shall be subject to the statute of limitations applicable under the governing law specified in Section 3.3.
ARTICLE XI — DOCUMENT RETENTION AND DESTRUCTION
Section 11.1 — Post-Arbitration Document Retention. Each Party shall retain all documents, materials, evidence, submissions, transcripts, orders, awards, and other records produced, created, or exchanged in any Proceeding for a minimum of seven (7) years follo
ARTICLE XII — GENERAL PROVISIONS
Section 12.1 — Notices. All notices, requests, demands, and other communications under this Agreement shall be delivered in the manner provided in Section 11.4 of the Co-Investment Agreement to the Parties at the addresses set forth therein or such other addre
Section 12.2 — Entire Agreement. This Agreement constitutes the entire agreement between the Parties with respect to the subject matter hereof and supersedes all prior negotiations, representations, warranties, commitments, offers, and agreements (whether oral
Section 12.3 — Amendment and Waiver. This Agreement may not be amended, modified, or supplemented except by a written instrument signed by both Parties. No waiver of any provision of this Agreement shall be effective unless in writing signed by the waiving Par
Section 12.4 — Severability. If any provision of this Agreement is held to be invalid, illegal, or unenforceable in any respect, such invalidity, illegality, or unenforceability shall not affect any other provision of this Agreement, and this Agreement shall b
Section 12.5 — Counterparts. This Agreement may be executed in counterparts, each of which shall be deemed an original, and all of which together shall constitute one and the same instrument. Execution and delivery of this Agreement by facsimile or electronic 
Section 12.6 — Relationship to Co-Investment Agreement. This Agreement is Exhibit F to and is incorporated into the Co-Investment Agreement. In the event of a conflict between the terms of this Agreement and the arbitration-related provisions of the Co-Investm
Section 12.7 — Survival. This Agreement shall survive the termination or expiration of the Co-Investment Agreement with respect to any Dispute arising prior to or upon such termination or expiration.
[Signature Page Follows]
IN WITNESS WHEREOF, the Parties have executed this Arbitration Agreement as of the date first written above.
WHITMORE CAPITAL FUND III LP
By: Whitmore Capital Partners LLC, its General Partner
By: ________
Name: ________
Title: ________
Date: ________
CASCADIAN GROWTH FUND LP
By: Cascadian Growth Management LLC, its General Partner
By: ________
Name: ________
Title: ________
Date: ________
Shell cwd was reset to .
[ASSISTANT] The accepted text reads correctly, but two leftovers remain: Sections 5.2 and 5.3 still say "the Arbitrator" where the defined term is now "Tribunal". I'll fix those and scan for any other residual ICC, Seattle, Washington, or sole-arbitrator references.
[ACTION] Bash {"command": "cd /tmp/build && python3 -I - <<'EOF'\ns = open('build_redline.py', encoding='utf-8').read()\nold = \" 40: [('The Arbitrator shall hold', 'The Tribunal shall hold'), ('as the Arbitrator deems', 'as the Tribunal deems')],\"\nnew = \" 40: [('The Arbitrator shall hold', 'The Tribunal shall hold'), ('as the Arbitrator deems', 'as the Tribunal deems'), ('directed by the Arbitrator.', 'directed by the Tribunal.')],\"\nassert s.count(old) == 1; s = s.replace(old, new)\nold = \" 41: [('The Arbitrator shall have the authority', 'The Tribunal shall have the authority'), ('The Arbitrator shall determine', 'The Tribunal shall determine')],\"\nnew = \" 41: [('The Arbitrator shall have the authority', 'The Tribunal shall have the authority'), ('The Arbitrator shall determine', 'The Tribunal shall determine'), ('such evidence as the Arbitrator deems', 'such evidence as the Tribunal deems')],\"\nassert s.count(old) == 1; s = s.replace(old, new)\nopen('build_redline.py', 'w', encoding='utf-8').write(s)\nEOF\npython3 -I build_redline.py >/dev/null && OUT=./output/redlined-arbitration-agreement.docx && pandoc \"$OUT\" -t plain --wrap=none --track-changes=accept -o accepted.txt && pandoc \"$OUT\" -t plain --wrap=none --track-changes=reject -o rejected.txt && diff <(grep -v '^$' orig_plain.txt | sed 's/[[:space:]]
[OBSERVATION]
REJECT_OK
12:WHEREAS, Whitmore Capital Fund III LP, a Delaware limited partnership ("Whitmore"), an investment vehicle managed by Whitmore Capital Partners LLC, a Delaware limited liability company, with its principal office at 34
32:"Arbitral Tribunal" or "Tribunal" means the three (3) Arbitrators, or the sole Arbitrator in the case of an Expedited Dispute, appointed pursuant to Article IV of this Agreement to resolve a Dispute.
75:Section 4.1 — Number of Arbitrators. The arbitration shall be conducted by a three (3)-member Tribunal, each member of which shall be an "Arbitrator" appointed in accordance with Section 4.2, except that an Expedited 
81:Section 4.3 — Qualifications. Each Arbitrator (including any sole Arbitrator) shall be a neutral individual independent of the Parties and shall: (a) have at least fifteen (15) years of professional experience in priv
96:Section 5.5 — Expedited Disputes. Notwithstanding Sections 4.1, 5.1, and 8.1, the following shall apply to any Dispute concerning (i) the timing, amount, validity, or enforceability of a capital call, (ii) the exercis
Shell cwd was reset to .
[ASSISTANT] The remaining hits are intentional: Cascadian's Seattle office address in the recitals and the expedited sole arbitrator. Next I'll check whether I can render the file to confirm it displays correctly.
[ACTION] Bash {"command": "which soffice libreoffice 2>/dev/null; ls /Applications 2>/dev/null | grep -i libre; echo \"exit=$?\"", "description": "Check whether LibreOffice is available for rendering"}
[OBSERVATION]
soffice not found
libreoffice not found
LibreOffice.app
exit=0
[ACTION] Bash {"command": "cd /tmp/build && OUTDIR=/tmp/build/render && rm -rf $OUTDIR && mkdir -p $OUTDIR && cp ./output/redlined-arbitration-agreement.docx $OUTDIR/r.docx && timeout 120 /Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf --outdir $OUTDIR $OUTDIR/r.docx >/dev/null 2>&1; ls -la $OUTDIR; which pdftoppm && pdftoppm -r 60 -f 3 -l 3 -png $OUTDIR/r.pdf $OUTDIR/p && ls $OUTDIR", "description": "Render redline to PDF with LibreOffice for visual check"}
[OBSERVATION]
Exit code 1
total 112
drwxr-xr-x@  3 me  wheel     96 Oct 19 11:53 .
drwxr-xr-x@ 17 me  wheel    544 Oct 19 11:53 ..
-rw-r--r--@  1 me  wheel  55302 Oct 19 11:53 r.docx
/Users/me/.local/bin/pdftoppm
I/O Error: Couldn't open file '/tmp/build/render/r.pdf': No such file or directory.
[ACTION] Bash {"command": "cd /tmp/build/render && timeout 180 /Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf --outdir /tmp/build/render /tmp/build/render/r.docx 2>&1 | tail -5; ls /tmp/build/render", "description": "Retry LibreOffice PDF conversion with error output"}
[OBSERVATION]
(eval):1: command not found: timeout
r.docx
Shell cwd was reset to .
[ACTION] Bash {"command": "cd /tmp/build/render && /Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf --outdir /tmp/build/render /tmp/build/render/r.docx 2>&1 | tail -3; ls /tmp/build/render; pdftoppm -r 70 -f 3 -l 3 -png r.pdf p 2>/dev/null && ls", "description": "Convert redline to PDF and rasterize one page"}
[OBSERVATION]
Exit code 1
libc++abi: terminating due to uncaught exception of type com::sun::star::deployment::DeploymentException
Unspecified Application Error
r.docx
[ASSISTANT] LibreOffice fails in this environment (a deployment exception), so I can't render the redline visually. I've verified it structurally instead: the XML parses, pandoc reads both the accepted and rejected views, and reject-all matches the original exactly. I'll note that gap in the summary.

Next is the cover memo, organized by the playbook's Critical / Important / Recommended tiers, with the GC decision points called out.
[ACTION] Bash {"command": "cat > /tmp/build/memo.md <<'EOF'\n**PRIVILEGED & CONFIDENTIAL \u2014 ATTORNEY-CLIENT COMMUNICATION / ATTORNEY WORK PRODUCT**\n\n**DRAFT FOR D. OSTRANDER REVIEW**\n\n# MEMORANDUM\n\n|  |  |\n|---|---|\n| **To:** | Rebecca Stadler, General Counsel, Whitmore Capital Partners LLC |\n| **From:** | Hargrove, Wynn & Calloway LLP (Vantage deal team) |\n| **Date:** | January [\u25cf], 2025 |\n| **Re:** | Vantage Specialty Chemicals / Cascadian co-investment: markup of proposed Arbitration Agreement (Exhibit F to Co-Investment Agreement) |\n\n## 1. Summary\n\nPinnacle Winterhaven's January 8 draft departs from the Whitmore Arbitration Playbook (v3.0, Nov. 15, 2024) on 18 of the playbook's 20 topics. Only scope (\u00a77) and English language (\u00a721) are acceptable as drafted. The redline (`redlined-arbitration-agreement.docx`) makes every change as a tracked revision, with bracketed notes that cite the playbook section and classify each position as Required, Preferred, or Fallback.\n\nYour three priorities are addressed as follows:\n\n1. **Three-member panel** (\u00a74): sole arbitrator replaced; party-appointed arbitrators select the chair; AAA backstop.\n2. **Court interim relief** (\u00a76): waiver deleted; carve-out and emergency arbitrator provisions added.\n3. **Expedited track** (\u00a75.5): capital call, drag-along, and buy-sell disputes; sole arbitrator; 45-day award.\n\nThe internal notes in the redline reveal fallback positions. **The redline must not go to Pi
[OBSERVATION]
None 35234
    1256
Shell cwd was reset to .
[ASSISTANT] The memo converted cleanly. As a final check, I'll read both deliverables back through the workspace's own `read_doc.py` and confirm the output folder contents.
[ACTION] Bash {"command": "for f in output/redlined-arbitration-agreement.docx output/markup-cover-memo.docx; do python3 scripts/read_doc.py \"$f\" | wc -w; done; ls -la output; python3 -I -c \"print('ok')\"", "description": "Read back both deliverables with read_doc.py and list output"}
[OBSERVATION]
    6938
    1262
total 144
drwxr-xr-x@ 4 me  staff    128 Oct 19 11:54 .
drwxr-xr-x@ 6 me  staff    192 Oct 19 11:47 ..
-rw-r--r--@ 1 me  staff  15720 Oct 19 11:54 markup-cover-memo.docx
-rw-r--r--@ 1 me  staff  55302 Oct 19 11:53 redlined-arbitration-agreement.docx
ok
[ASSISTANT] Both deliverables are in `output/`:

- **`redlined-arbitration-agreement.docx`**: the Cascadian form with real Word tracked changes on the original file, plus bracketed notes citing the playbook and classifying each position as Required, Preferred, or Fallback. Rejecting all changes reproduces the original text exactly.
- **`markup-cover-memo.docx`**: a memo to Rebecca Stadler with the changes grouped as Critical, Important, and Recommended (per playbook §22), the open decisions, and the assumptions.

**Main positions taken:** AAA instead of ICC; Atlanta seat instead of Seattle; Delaware law instead of Washington; a three-member panel; the court-relief waiver deleted with a carve-out and emergency arbitrator; the expedited track for capital call, drag-along, and buy-sell disputes; the one-year limitations period deleted; the destruction clause replaced with seven-year retention; and confidentiality, damages waiver, class waiver, prevailing-party fees, and optional appellate review added.

**Needs attention before anything goes out:**

- **Do not send this redline to Pinnacle Winterhaven as it is.** The notes disclose the playbook, the Required/Fallback classifications, and Whitmore's fallback positions. I did not produce a clean external version; that should be done after Rebecca's review.
- **The playbook's expedited deadlines conflict.** A 10-business-day appointment plus a hearing up to 30 days after appointment can place the hearing about day 44, leaving about one day before the 45-day award. I kept the playbook terms and left the outside hearing date as a bracketed placeholder for the GC to set.
- **Confidentiality exceptions omit LP reporting,** though the playbook's own record-retention rationale cites LP reporting. The GC should decide whether to request an exception.
- **Approved forms and rules titles are unverified.** Playbook §23 says to use the GC's approved language for the inserted provisions, which isn't in the file, so I drafted from the playbook text. I also could not verify the current AAA rule titles.
- **The CIA was not in the file.** Its governing law, dispute clause, and the §11.4 notices cross-reference are unchecked.
- **Transmittal discrepancy.** Pinnacle's cover email is addressed to a misspelled firm domain and comes from a different firm domain than its signature. Worth confirming before responding.

**Verification gap:** LibreOffice fails in this environment, so I could not render the redline visually. I checked the XML structure, the accept and reject views, and read-back through `read_doc.py`. Please open it in Word once to confirm the tracked changes display as expected.