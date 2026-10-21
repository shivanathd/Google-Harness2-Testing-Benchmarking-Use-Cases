[ACTION] Skill {"skill": "arbitration-playbook-redline"}
[OBSERVATION]
Launching skill: arbitration-playbook-redline
[ACTION] Bash {"command": "find . -path ./.claude -prune -o -type f -print | head -100 && ls -la output 2>/dev/null; python3 -c \"import docx, sys; print('python-docx ok')\" 2>&1; ls .claude/skills/arbitration-playbook-redline 2>/dev/null", "description": "List workspace files and tooling"}
[OBSERVATION]
./scripts/read_doc.py
./documents/cascadian-counsel-cover-email.eml
./documents/proposed-arbitration-agreement.docx
./documents/whitmore-internal-instructions.eml
./documents/whitmore-arbitration-playbook.docx
./CLAUDE.md
total 0
drwxr-xr-x@ 2 me  staff   64 Oct 19 11:47 .
drwxr-xr-x@ 7 me  staff  224 Oct 19 12:01 ..
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import docx, sys; print('python-docx ok')
    ^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'docx'
SKILL.md
[ACTION] Bash {"command": "cat scripts/read_doc.py | head -60; echo ----; python3 scripts/read_doc.py documents/proposed-arbitration-agreement.docx > /tmp/agmt.txt 2>&1; wc -l /tmp/agmt.txt; python3 scripts/read_doc.py documents/whitmore-arbitration-playbook.docx > /tmp/playbook.txt 2>&1; wc -l /tmp/playbook.txt; wc -c documents/*.eml", "description": "Extract document text for reading"}
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
----
     155 /tmp/agmt.txt
     551 /tmp/playbook.txt
    5115 documents/cascadian-counsel-cover-email.eml
    7716 documents/whitmore-internal-instructions.eml
   12831 total
[ACTION] Bash {"command": "cat documents/whitmore-internal-instructions.eml; echo =====; cat documents/cascadian-counsel-cover-email.eml", "description": "Read both instruction emails"}
[OBSERVATION]
Exit code 1
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
(eval):1: ==== not found
[ACTION] Bash {"command": "cat documents/cascadian-counsel-cover-email.eml", "description": "Read counterparty cover email"}
[OBSERVATION]
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
[ACTION] Bash {"command": "cat /tmp/agmt.txt", "description": "Read proposed agreement text"}
[OBSERVATION]
**EXHIBIT F TO CO-INVESTMENT AGREEMENT**

**ARBITRATION AGREEMENT**

Dated as of January 15, 2025

This Arbitration Agreement (this \"**Agreement**\") is entered into as of January 15, 2025, by and between the following parties in connection with that certain Co-Investment Agreement dated as of even date herewith (the \"**Co-Investment Agreement**\"). Capitalized terms used but not otherwise defined herein shall have the meanings ascribed to them in the Co-Investment Agreement.

**[RECITALS]{.underline}**

**WHEREAS**, Whitmore Capital Fund III LP, a Delaware limited partnership (\"**Whitmore**\"), an investment vehicle managed by Whitmore Capital Partners LLC, a Delaware limited liability company, with its principal office at 3400 Peachtree Road NE, Suite 1200, Atlanta, GA 30326, and Cascadian Growth Fund LP, a Delaware limited partnership (\"**Cascadian**\"), managed by its general partner, Cascadian Growth Management LLC, a Delaware limited liability company, with its principal office at 1501 Fourth Avenue, Suite 3700, Seattle, WA 98101 (each, a \"**Party**\" and together, the \"**Parties**\"), have entered into that certain Co-Investment Agreement dated as of January 15, 2025 (the \"**Co-Investment Agreement**\");

**WHEREAS**, pursuant to the Co-Investment Agreement, the Parties have agreed to jointly acquire a controlling interest (approximately 72%) of Vantage Specialty Chemicals Inc., a Delaware corporation headquartered at 10200 Bellaire Boulevard, Suite 400, Houston, TX 77072 (the \"**Target**\" or the \"**Company**\"), at a total enterprise value of \$680,000,000, with Whitmore contributing \$195,000,000 in equity for a 48% equity stake and Cascadian contributing \$130,000,000 in equity for a 24% equity stake, for total equity of \$325,000,000, with the remaining \$355,000,000 in debt financing;

**WHEREAS**, the Co-Investment Agreement governs, among other things, governance rights, drag-along and tag-along rights, transfer restrictions, and capital call mechanics relating to the Parties\' investment in the Company; and

**WHEREAS**, the Parties desire to establish the terms and procedures by which disputes arising under or in connection with the Co-Investment Agreement shall be resolved.

**NOW, THEREFORE**, in consideration of the mutual covenants and agreements set forth in the Co-Investment Agreement, and for other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the Parties agree as follows:

**[ARTICLE I --- DEFINITIONS]{.underline}**

As used in this Agreement, the following terms shall have the meanings set forth below:

\"**Agreement**\" means this Arbitration Agreement, as it may be amended from time to time in accordance with its terms.

\"**Arbitral Tribunal**\" or \"**Tribunal**\" means the arbitrator or arbitrators appointed pursuant to Article IV of this Agreement to resolve a Dispute.

\"**Award**\" means any interim, partial, or final award rendered by the Arbitral Tribunal in connection with any Proceedings.

\"**Claimant**\" means the Party initiating a Proceeding by filing a request for arbitration.

\"**Co-Investment Agreement**\" or \"**CIA**\" has the meaning set forth in the Recitals.

\"**Company**\" means Vantage Specialty Chemicals Inc., a Delaware corporation.

\"**Dispute**\" means any dispute, controversy, or claim arising out of, relating to, or in connection with this Agreement or the Co-Investment Agreement, including any question regarding the existence, formation, validity, interpretation, performance, breach, or termination thereof.

\"**ICC**\" means the International Chamber of Commerce.

\"**ICC Rules**\" means the Rules of Arbitration of the International Chamber of Commerce in effect at the time of commencement of the arbitration.

\"**Party**\" and \"**Parties**\" have the meanings set forth in the Recitals.

\"**Proceedings**\" means any arbitration proceedings commenced pursuant to this Agreement.

\"**Respondent**\" means the Party against whom a request for arbitration is filed.

\"**Seat**\" means Seattle, Washington, which shall be the juridical seat of any arbitration conducted under this Agreement.

**[ARTICLE II --- AGREEMENT TO ARBITRATE; SCOPE]{.underline}**

**Section 2.1 --- Agreement to Arbitrate.** Any and all disputes, controversies, or claims arising out of, relating to, or in connection with this Agreement or the Co-Investment Agreement, including but not limited to the formation, validity, interpretation, performance, breach, or termination thereof (each, a \"**Dispute**\"), shall be exclusively and finally resolved by binding arbitration administered by the International Chamber of Commerce in accordance with the ICC Rules in effect at the time of the filing of the request for arbitration. The Parties acknowledge and agree that this Agreement evidences a transaction involving commerce and that the Federal Arbitration Act, 9 U.S.C. §§ 1--16, shall govern the interpretation and enforcement of this Agreement.

**Section 2.2 --- Exclusive Remedy.** Arbitration under this Agreement shall be the exclusive remedy for any Dispute, and no Party shall institute any action or proceeding in any court with respect to any Dispute, except as expressly provided herein.

**[ARTICLE III --- SEAT, LANGUAGE, AND GOVERNING LAW]{.underline}**

**Section 3.1 --- Seat of Arbitration.** The seat (legal place) of arbitration shall be Seattle, Washington. Any hearings shall be conducted at the Seat unless otherwise agreed by the Parties or ordered by the Arbitral Tribunal.

**Section 3.2 --- Language.** The language of the arbitration shall be English. All submissions, correspondence, evidence, and hearings shall be conducted in English.

**Section 3.3 --- Governing Law.** This Agreement shall be governed by and construed in accordance with the laws of the State of Washington, without regard to its conflict of laws principles.

**[ARTICLE IV --- ARBITRATOR APPOINTMENT AND QUALIFICATIONS]{.underline}**

**Section 4.1 --- Number of Arbitrators.** The arbitration shall be conducted by a sole arbitrator (the \"**Arbitrator**\") appointed in accordance with the ICC Rules.

**Section 4.2 --- Appointment Procedure.** The Parties shall endeavor to agree upon a mutually acceptable Arbitrator within thirty (30) days following the filing of the request for arbitration. If the Parties are unable to agree upon the Arbitrator within such thirty (30)-day period, the Arbitrator shall be appointed by the ICC in accordance with the ICC Rules.

**Section 4.3 --- Qualifications.** The Arbitrator shall be a neutral individual independent of the Parties.

**[ARTICLE V --- ARBITRATION PROCEDURES]{.underline}**

**Section 5.1 --- Discovery.** Discovery shall be conducted in accordance with the ICC Rules, without modification. The Arbitrator shall have the authority to manage and limit discovery as the Arbitrator deems appropriate in the interests of efficiency and proportionality.

**Section 5.2 --- Hearings.** The Arbitrator shall hold hearings as the Arbitrator deems necessary and appropriate. Hearings shall be held at the Seat unless otherwise agreed by the Parties or directed by the Arbitrator.

**Section 5.3 --- Evidence.** The Arbitrator shall have the authority to receive and consider such evidence as the Arbitrator deems relevant and material, including documentary evidence, witness testimony, and expert reports. The Arbitrator shall determine the admissibility, relevance, materiality, and weight of any evidence offered.

**[ARTICLE VI --- INTERIM AND EMERGENCY RELIEF]{.underline}**

**Section 6.1 --- Waiver of Court Relief.** The Parties hereby expressly waive any right to seek provisional or interim measures, including but not limited to temporary restraining orders, preliminary injunctions, attachments, or any other form of interim or conservatory relief, from any court of competent jurisdiction in connection with any Dispute subject to arbitration under this Agreement. All requests for provisional or interim measures shall be directed exclusively to the Arbitral Tribunal. The Parties acknowledge that this waiver is knowing, voluntary, and made in consideration of the mutual benefits of resolving all aspects of any Dispute through the arbitral process established herein.

**[ARTICLE VII --- CONSOLIDATION AND JOINDER]{.underline}**

**Section 7.1 --- Consolidation.** The Tribunal may, at the request of either Party, consolidate this arbitration with any other arbitration arising out of or in connection with the Co-Investment Agreement or any other agreement between the Parties or involving a party to this Agreement, provided that the Tribunal determines that common questions of fact or law exist. The Tribunal shall have sole discretion to determine whether consolidation is appropriate and shall consider the stage of the existing proceedings, the efficiency of consolidation, and any prejudice to the Parties.

**Section 7.2 --- Joinder of Third Parties.** Third parties may be joined to the arbitration at the discretion of the Tribunal, upon request by either Party, without the requirement of consent of all parties to the arbitration or of the party to be joined, provided that the Tribunal determines that such joinder is necessary for the complete resolution of the Dispute. The Tribunal shall have full authority to establish the terms and conditions of any such joinder, including with respect to the allocation of costs associated therewith.

**[ARTICLE VIII --- AWARD]{.underline}**

**Section 8.1 --- Timing and Form of Award.** The Arbitrator shall use best efforts to issue a reasoned award within one hundred twenty (120) days of the close of Proceedings. The award shall be in writing and shall set forth the Arbitrator\'s reasoning. Failure to render the award within such period shall not affect the validity of the award or the jurisdiction of the Arbitrator.

**Section 8.2 --- Finality.** The award of the Arbitrator shall be final and binding upon the Parties and shall not be subject to appeal, except as otherwise provided by applicable law. Judgment upon the award may be entered in any court of competent jurisdiction. The Parties hereby waive, to the fullest extent permitted by law, any right to appeal or challenge the award, except on the limited grounds set forth in the Federal Arbitration Act.

**Section 8.3 --- Remedies.** The Arbitrator shall have the authority to award any remedy or relief that a court of competent jurisdiction could grant, including but not limited to specific performance, injunctive relief, and monetary damages. The Arbitrator shall not be limited in the types or amounts of damages that may be awarded.

**[ARTICLE IX --- COSTS AND FEES]{.underline}**

**Section 9.1 --- Allocation of Costs.** Each Party shall bear its own costs and expenses of the arbitration, including but not limited to attorneys\' fees, expert fees, witness fees, and all other costs incurred in connection with the arbitration, regardless of the outcome.

**Section 9.2 --- Administrative Costs.** The administrative fees and expenses of the ICC and the fees and expenses of the Arbitrator shall be shared equally by the Parties, unless the Arbitrator determines otherwise in the award.

**[ARTICLE X --- LIMITATIONS PERIOD]{.underline}**

**Section 10.1 --- Statute of Limitations.** All claims subject to arbitration under this Agreement must be commenced by the filing of a request for arbitration within one (1) year of the date on which the claiming Party knew or should have known of the facts giving rise to the claim. Any claim not commenced within such one (1)-year period shall be forever barred and waived. The Parties acknowledge that this limitations period may be shorter than the limitations period otherwise applicable under governing law and agree that this shortened period is reasonable and enforceable.

**[ARTICLE XI --- DOCUMENT RETENTION AND DESTRUCTION]{.underline}**

**Section 11.1 --- Post-Arbitration Document Handling.** The Parties agree that, within thirty (30) days following the issuance of the final award (or, if applicable, the resolution of any proceeding to confirm or vacate the award), each Party shall destroy or cause to be destroyed all documents, materials, evidence, submissions, transcripts, and other records produced, created, or exchanged during the arbitration, and shall certify such destruction in writing to the other Party. This obligation shall survive the termination of this Agreement and shall be binding upon each Party\'s officers, directors, employees, agents, and representatives.

**[ARTICLE XII --- GENERAL PROVISIONS]{.underline}**

**Section 12.1 --- Notices.** All notices, requests, demands, and other communications under this Agreement shall be delivered in the manner provided in Section 11.4 of the Co-Investment Agreement to the Parties at the addresses set forth therein or such other address as a Party may designate in writing from time to time in accordance with the provisions of the Co-Investment Agreement.

**Section 12.2 --- Entire Agreement.** This Agreement constitutes the entire agreement between the Parties with respect to the subject matter hereof and supersedes all prior negotiations, representations, warranties, commitments, offers, and agreements (whether oral or written) with respect to the subject matter hereof.

**Section 12.3 --- Amendment and Waiver.** This Agreement may not be amended, modified, or supplemented except by a written instrument signed by both Parties. No waiver of any provision of this Agreement shall be effective unless in writing signed by the waiving Party. No failure or delay by any Party in exercising any right, power, or privilege hereunder shall operate as a waiver thereof, nor shall any single or partial exercise thereof preclude any other or further exercise thereof or the exercise of any other right, power, or privilege.

**Section 12.4 --- Severability.** If any provision of this Agreement is held to be invalid, illegal, or unenforceable in any respect, such invalidity, illegality, or unenforceability shall not affect any other provision of this Agreement, and this Agreement shall be construed as if such invalid, illegal, or unenforceable provision had never been contained herein. The Parties shall negotiate in good faith to replace any such invalid, illegal, or unenforceable provision with a valid, legal, and enforceable provision that, to the greatest extent possible, achieves the original intent and economic effect of the invalid provision.

**Section 12.5 --- Counterparts.** This Agreement may be executed in counterparts, each of which shall be deemed an original, and all of which together shall constitute one and the same instrument. Execution and delivery of this Agreement by facsimile or electronic transmission (including in .pdf format) shall be deemed to be, and shall have the same legal effect as, execution and delivery of an original.

**Section 12.6 --- Relationship to Co-Investment Agreement.** This Agreement is Exhibit F to and is incorporated into the Co-Investment Agreement. In the event of a conflict between the terms of this Agreement and the arbitration-related provisions of the Co-Investment Agreement, the terms of this Agreement shall control.

**Section 12.7 --- Survival.** This Agreement shall survive the termination or expiration of the Co-Investment Agreement with respect to any Dispute arising prior to or upon such termination or expiration.

*\[Signature Page Follows\]*

**IN WITNESS WHEREOF**, the Parties have executed this Arbitration Agreement as of the date first written above.

**WHITMORE CAPITAL FUND III LP**

By: Whitmore Capital Partners LLC, its General Partner

By: **\_\_\_\_\_\_\_\_**

Name: **\_\_\_\_\_\_\_\_**

Title: **\_\_\_\_\_\_\_\_**

Date: **\_\_\_\_\_\_\_\_**

**CASCADIAN GROWTH FUND LP**

By: Cascadian Growth Management LLC, its General Partner

By: **\_\_\_\_\_\_\_\_**

Name: **\_\_\_\_\_\_\_\_**

Title: **\_\_\_\_\_\_\_\_**

Date: **\_\_\_\_\_\_\_\_**
[ACTION] Bash {"command": "sed -n 1,280p /tmp/playbook.txt", "description": "Read playbook first half"}
[OBSERVATION]
**PRIVILEGED & CONFIDENTIAL --- ATTORNEY-CLIENT PRIVILEGED / WORK PRODUCT**

**[WHITMORE CAPITAL PARTNERS LLC]{.underline}**

**[ARBITRATION PLAYBOOK: POLICY & GUIDANCE FOR OUTSIDE COUNSEL]{.underline}**

**From:** Rebecca Stadler, General Counsel Whitmore Capital Partners LLC 3400 Peachtree Road NE, Suite 1200 Atlanta, GA 30326

**To:** Outside Counsel Hargrove, Wynn & Calloway LLP 195 Peachtree Street NE, Suite 4500 Atlanta, GA 30303 *Attention:* David Ostrander, Partner; Priya Nakamura, Associate

**Date:** Last Updated November 15, 2024

**Version:** 3.0

**Supersedes:** Version 2.0 (March 2022)

**[Section 1: Purpose and Scope]{.underline}**

This memorandum establishes Whitmore Capital Partners LLC\'s (\"Whitmore\" or the \"Firm\") mandatory policies, preferred positions, and acceptable fallback positions for arbitration provisions in transaction documents. It is intended to serve as a comprehensive reference for outside counsel when drafting, reviewing, negotiating, or marking up arbitration agreements and dispute resolution provisions.

**Applicability.** This playbook applies to all arbitration agreements, arbitration clauses, and dispute resolution provisions in connection with investments made by Whitmore Capital Fund III LP or any other Whitmore-managed fund vehicle, including but not limited to co-investment agreements, joint venture agreements, side letters, limited partnership agreements, subscription agreements, and any ancillary agreements containing dispute resolution provisions.

**Compliance Requirement.** Outside counsel must consult this playbook before drafting or reviewing any arbitration provision. Any departure from a position designated as \"Required\" must be flagged for approval by the General Counsel before acceptance. No Required position may be conceded in negotiations without express, prior written authorization from the General Counsel.

**Organization.** This playbook is organized by topic. Each topic designates positions according to the following classification hierarchy:

> • **Required** --- Non-negotiable absent General Counsel approval. These positions reflect Whitmore\'s firm policy and may not be compromised without escalation.
>
> • **Preferred** --- Target position in negotiations. Outside counsel should pursue these positions vigorously but may accept a Fallback position if necessary without escalation.
>
> • **Fallback** --- Acceptable compromise if the Required or Preferred position cannot be obtained through negotiation.

**Context.** Whitmore manages approximately \$3.8 billion in committed capital across three fund vehicles. The Firm\'s typical co-investment transaction sizes range from \$100 million to \$500 million in equity commitments. The stakes in arbitrated disputes arising from these transactions can be substantial, and the procedural framework governing those disputes has a material impact on outcomes. This playbook is designed to protect fund investors and ensure procedural fairness in every arbitrated dispute.

**[Section 2: Administering Institution]{.underline}**

**Required:** For all domestic U.S. transactions --- including co-investment agreements, joint venture agreements, and side letters --- the administering institution must be the **American Arbitration Association (\"AAA\")** under the **Commercial Arbitration Rules**.

**Preferred:** AAA Commercial Arbitration Rules (most current version as of the date the dispute is submitted to arbitration).

**Fallback:** JAMS Comprehensive Arbitration Rules and Procedures is acceptable as an alternative if the counterparty objects to AAA. JAMS provides a credible domestic commercial arbitration platform with a qualified roster of arbitrators.

**NOT ACCEPTABLE:** The International Chamber of Commerce (\"ICC\") is reserved exclusively for cross-border or international transactions --- that is, transactions in which at least one party is organized or headquartered outside the United States, or the underlying assets are located outside the United States. The ICC shall **never** be designated as the administering institution for purely domestic U.S. co-investment transactions.

**Rationale:**

> • AAA has the deepest bench of domestic commercial arbitrators with private equity, mergers and acquisitions, and corporate finance experience.
>
> • ICC administrative fees are disproportionately high for domestic matters, as they are calculated based on the amount in dispute using fee scales designed for international proceedings.
>
> • ICC procedural rules are designed for international disputes and introduce unnecessary complexity in domestic contexts, including requirements such as the Terms of Reference, the ICC Court\'s scrutiny of draft awards, and other procedural mechanisms that add cost and delay without corresponding benefit in a purely domestic U.S. proceeding.
>
> • AAA\'s procedural framework is more streamlined for domestic commercial disputes, and its case management personnel are experienced with U.S. private equity and M&A matters.

**[Section 3: Seat of Arbitration]{.underline}**

**Required:** The seat (legal place) of arbitration must be **Atlanta, Georgia** --- Whitmore\'s home jurisdiction.

**Preferred:** Atlanta, Georgia.

**Fallback:** If the counterparty objects to Atlanta, **New York, New York** is acceptable as a neutral forum. New York provides a well-developed body of arbitration law under the New York Convention and the Federal Arbitration Act, and is generally perceived as a neutral commercial arbitration venue.

**NOT ACCEPTABLE:** The counterparty\'s home jurisdiction. Under no circumstances should the seat be located in a jurisdiction where the counterparty (or its general partner or management company) is headquartered. This restriction is categorical and applies regardless of the counterparty\'s identity. Agreeing to the counterparty\'s home jurisdiction creates an inherent advantage for the counterparty in terms of familiarity with local courts (for enforcement, provisional relief, and vacatur proceedings), convenience for the counterparty\'s personnel and counsel, and potential perception of home-court bias.

**Rationale:**

> • The seat of arbitration determines the supervisory court for vacatur and enforcement proceedings under the Federal Arbitration Act, 9 U.S.C. §§ 1--16.
>
> • Whitmore\'s executives, internal documents, and primary counsel are located in Atlanta, and designating Atlanta as the seat reduces cost and disruption to fund operations.
>
> • New York is acceptable as a fallback because of the depth and sophistication of its judiciary, its extensive body of case law on arbitration, and its widely recognized neutrality as a dispute resolution forum.

**Hearing Location Note:** The physical location of hearings may differ from the seat if mutually convenient, but the legal seat governs the procedural law applicable to the arbitration, including the standards for judicial review, vacatur, and enforcement.

**[Section 4: Number of Arbitrators and Selection Mechanics]{.underline}**

**Required:** For any dispute where the amount in controversy exceeds **\$10 million**, the arbitration must be conducted before a **three-member arbitral tribunal**. Given that Whitmore\'s typical transaction sizes range from \$100 million to \$500 million in equity, virtually all disputes arising from co-investment agreements will exceed this threshold.

**Preferred:** Three-member panel with the following selection mechanics:

> \(a\) Each party (or side, if multiple parties are aligned as claimant or respondent) shall appoint one arbitrator within thirty (30) days of the filing of the demand for arbitration.
>
> \(b\) The two party-appointed arbitrators shall jointly select the chair (presiding arbitrator) within twenty (20) days of their appointment.
>
> \(c\) If the two party-appointed arbitrators cannot agree on a chair within the twenty (20) day period, the administering institution (AAA, or JAMS if applicable) shall appoint the chair from its roster of qualified arbitrators.

**Fallback:** A sole arbitrator is acceptable only for disputes where the amount in controversy is **\$10 million or less**. Even in such cases, the sole arbitrator must meet all of the qualification requirements set forth in Section 5.

**Rationale:**

> • A three-member panel provides a structural check against any single arbitrator\'s potential bias, error, or idiosyncratic interpretation of the governing documents.
>
> • Three-member panels are standard for high-value commercial disputes and are the prevailing norm in private equity and M&A arbitration.
>
> • Party appointment of co-arbitrators allows each side meaningful participation in tribunal composition, which enhances the perceived legitimacy and fairness of the process.
>
> • The \$10 million threshold is set deliberately low to ensure that panel composition applies to virtually all fund-level disputes. A dispute arising from a \$325 million co-investment, for example, plainly warrants a three-member panel.

**[Section 5: Arbitrator Qualifications]{.underline}**

**Required:** All arbitrators --- whether serving as a sole arbitrator or as a member of a three-member panel --- must satisfy **all** of the following minimum qualifications:

> 1\. **Experience:** A minimum of **fifteen (15) years** of professional experience in **private equity, mergers and acquisitions, or corporate finance**. Qualifying experience includes practice as an attorney, investment banker, or financial advisor in these fields, or service as an arbitrator in disputes involving these fields.
>
> 2\. **Roster Membership:** The arbitrator must be a member of the roster (panel) of the administering institution --- i.e., AAA\'s National Roster of Arbitrators or, if the administering institution is JAMS, the JAMS panel of neutrals.
>
> 3\. **Conflict-Free:** The arbitrator must not have had any professional, financial, or personal relationship with any party to the arbitration, any affiliate of a party, or any counsel of record within the **prior five (5) years**. This lookback period applies to direct and indirect relationships, including but not limited to service as counsel, advisor, board member, investor, consultant, or arbitrator in a proceeding involving any party, any affiliate of a party, or any counsel of record.

**Preferred:** In addition to the requirements above, Whitmore prefers arbitrators who have served as arbitrators in at least three (3) prior disputes involving private equity co-investment or joint venture agreements.

**Fallback:** If the counterparty objects to the 15-year experience requirement, Whitmore will accept a minimum of **ten (10) years** of qualifying experience, but only with prior General Counsel approval.

**Rationale:**

> • Private equity co-investment disputes involve complex governance, valuation, and contractual interpretation issues that require specialized knowledge. Generalist commercial arbitrators may lack the sophistication to handle capital call mechanics, waterfall calculations, drag-along and tag-along provisions, management fee offsets, clawback obligations, and other PE-specific issues.
>
> • The 5-year conflict lookback is essential to ensure independence and impartiality given the interconnected nature of the private equity industry, where a relatively small number of firms, advisors, and counsel participate across overlapping transactions.

**[Section 6: Governing Law]{.underline}**

**Required:** The governing law of the arbitration agreement itself --- as well as the underlying co-investment agreement --- must be the **law of the State of Delaware**, without regard to conflict-of-laws principles.

**Preferred:** Delaware law. Delaware is the jurisdiction of organization for most Whitmore fund vehicles and portfolio companies, has the most well-developed body of corporate and commercial law in the United States, and is the standard choice of law for private equity transactions.

**Fallback:** **New York law** is acceptable as an alternative if the counterparty objects to Delaware. New York provides a similarly developed body of commercial law and a sophisticated judiciary with extensive experience interpreting complex financial agreements.

**NOT ACCEPTABLE:** The counterparty\'s home-state law. Whitmore\'s policy **categorically prohibits** agreeing to have the arbitration agreement (or the underlying transaction documents) governed by the law of the state where the counterparty is headquartered. This prohibition avoids: (a) unfamiliarity with the governing law for Whitmore\'s counsel, (b) potential counterparty advantages arising from local law nuances or favorable precedent, and (c) inconsistency with the governing law of the underlying transaction documents, which are typically governed by Delaware law.

**Rationale:**

> • Consistency with the governing law of the co-investment agreement and related transaction documents (which, in virtually all Whitmore transactions, are governed by Delaware law).
>
> • Depth of Delaware case law on contractual interpretation, arbitrability, and enforceability of arbitration provisions.
>
> • Avoidance of the counterparty\'s home-court advantage.

**Note on Statute of Limitations:** Outside counsel should be aware that Delaware has a **three (3) year** statute of limitations for breach of contract claims not under seal (10 Del. C. § 8106), while New York has a **six (6) year** statute of limitations for breach of contract claims (N.Y. C.P.L.R. § 213). These differences should be considered when negotiating contractual limitations periods. *See* Section 15 for Whitmore\'s policy on statute of limitations.

**[Section 7: Scope of Arbitration]{.underline}**

**Required:** The arbitration clause should cover **all disputes** arising out of, relating to, or in connection with the co-investment agreement and any ancillary agreements, including disputes regarding formation, validity, interpretation, performance, breach, and termination.

Broad scope clauses are acceptable and standard. Whitmore does not impose any restriction on the breadth of the scope clause. A comprehensive scope clause reduces the risk of jurisdictional challenges and parallel court proceedings.

**Note:** Even with a broad scope clause, certain categories of disputes are subject to expedited treatment under Section 17 of this playbook.

**[Section 8: Discovery Limitations]{.underline}**

**Required:** Discovery must be limited as follows:

> • **Fact Depositions:** Each side may take up to **three (3) fact depositions**, each not to exceed **seven (7) hours** of testimony on the record.
>
> • **Document Requests:** Each side may serve up to **fifteen (15) document requests** (including subparts).
>
> • **Expert Discovery:** Each side may retain **one (1) testifying expert**. Expert reports must be exchanged **simultaneously** on a date set by the tribunal.

**Preferred:** The specific limitations set forth above should be stated expressly in the arbitration agreement itself, rather than being left to the rules of the administering institution or the tribunal\'s discretion.

**Fallback:** If the counterparty objects to specific numerical limits, agree that \"discovery shall be limited and proportional to the amounts in dispute, as determined by the tribunal\" --- but insist on the deposition cap (3 depositions per side) and expert cap (1 testifying expert per side) as non-negotiable minimums.

**Rationale:**

> • Unlimited or expansive discovery is the primary driver of cost and delay in arbitration. The limitations set forth above are calibrated to be sufficient for disputes of the complexity typical in co-investment matters while preventing the arbitration from devolving into *de facto* federal litigation discovery.
>
> • The simultaneous exchange of expert reports prevents gamesmanship and eliminates the tactical advantage of sequential rebuttal.
>
> • If a proposed arbitration agreement states only that discovery will follow the administering institution\'s rules \"without modification,\" this is **inadequate**. The playbook requires affirmative limitations to be incorporated into the agreement itself.

**[Section 9: Confidentiality]{.underline}**

**Required:** Every arbitration agreement must include a **mandatory confidentiality provision**. The absence of a confidentiality provision is unacceptable.

The confidentiality provision must cover each of the following categories of information:

> 1\. The existence of the arbitration proceeding.
>
> 2\. All submissions, briefs, motions, and pleadings filed in the arbitration.
>
> 3\. All evidence, testimony, exhibits, and documents produced or presented during the arbitration.
>
> 4\. All orders, rulings, and awards issued by the tribunal.
>
> 5\. All communications between the parties and the tribunal.

**Required Exceptions (and only these exceptions):**

> \(i\) Disclosures required by applicable law, regulation, or order of a court of competent jurisdiction, including but not limited to SEC reporting obligations, tax reporting, and regulatory inquiries.
>
> \(ii\) Disclosures necessary for the enforcement, confirmation, or vacatur of an arbitral award in proceedings before a court of competent jurisdiction.
>
> \(iii\) Disclosures to professional advisors --- including attorneys, accountants, and financial advisors --- who are subject to professional duties of confidentiality, provided that such advisors agree to be bound by the confidentiality obligations set forth in the arbitration agreement.

**Preferred:** Include a liquidated damages provision for breach of confidentiality, or at minimum, an express right to seek injunctive relief (including emergency relief) for any breach or threatened breach of the confidentiality obligations.

**Fallback:** If the counterparty resists the full scope set forth above, at minimum require confidentiality of (a) the award and (b) all financial information, trade secrets, and proprietary business information produced in the arbitration.

**Rationale:**

> • Whitmore\'s fund investors (limited partners) have explicit and implicit confidentiality expectations with respect to fund operations, performance, and disputes.
>
> • Public disclosure of arbitration proceedings could adversely affect deal flow, fund performance reporting, investor relations, and Whitmore\'s competitive position.
>
> • The exceptions are narrowly tailored to legal and regulatory necessity and do not authorize voluntary or discretionary disclosure.

**[Section 10: Interim and Emergency Relief]{.underline}**

**Required:** The arbitration agreement must **expressly preserve** each party\'s right to seek provisional, interim, or injunctive measures from **any court of competent jurisdiction** at any time before, during, or after the arbitration. This right must be stated as an **express carve-out** to the agreement to arbitrate and must make clear that seeking such relief does not constitute a waiver of the right to arbitrate.

**Required:** The agreement must incorporate the administering institution\'s **emergency arbitrator provisions** (e.g., AAA\'s Optional Rules for Emergency Measures of Protection or JAMS\'s equivalent emergency relief procedures).

**NOT ACCEPTABLE:** Any waiver, restriction, or limitation on a party\'s right to seek interim or provisional relief from a court. Express waivers of court-ordered provisional relief are **categorically prohibited** and must be **deleted** wherever found in a counterparty\'s proposed agreement.

**Preferred:** Include a specific statement that seeking court-ordered interim relief does not waive the right to arbitrate, is not inconsistent with the agreement to arbitrate, and shall not be deemed a submission to the jurisdiction of the court for any purpose other than the relief sought.

**Fallback:** None. This is a **non-negotiable** position. If the counterparty insists on a waiver of court relief, escalate to the General Counsel immediately. Do not accept any formulation that restricts, limits, conditions, or delays a party\'s right to seek court-ordered provisional measures.

**Rationale:**

> • Provisional court relief --- such as temporary restraining orders, preliminary injunctions, and asset-freezing orders --- may be necessary on an emergency basis to prevent irreparable harm before an arbitral tribunal can be constituted. Common scenarios in the co-investment context include:
>
> \(a\) Breach of non-compete or non-solicitation provisions by portfolio company management.
>
> \(b\) Unauthorized transfer of equity interests in violation of transfer restrictions, ROFR provisions, or lock-up periods.
>
> \(c\) Misappropriation of confidential information, trade secrets, or proprietary data.
>
> \(d\) Dissipation of assets or fraudulent transfers that may render a future arbitral award uncollectible.
>
> • Waiving the right to seek court-ordered provisional relief leaves Whitmore without any remedy during the weeks or months it takes to constitute a tribunal, during which irreparable harm may occur.
>
> • The emergency arbitrator mechanism provides an additional layer of interim protection but does **not** substitute for court relief. Emergency arbitrator orders may not be enforceable in the same manner as court orders, and not all administering institutions have emergency arbitrator provisions.
>
> • **Rebecca Stadler has specifically flagged this position as \"non-negotiable\" in client instructions for the current Vantage Specialty Chemicals Inc. transaction.**

**[Section 11: Consolidation]{.underline}**

**Required:** Consolidation of arbitration proceedings must require the **prior written consent of all parties to all proceedings** proposed to be consolidated. The tribunal must not have unilateral authority to order consolidation, and no single party may compel consolidation over the objection of another party.

**Preferred:** Same as Required.

**Fallback:** If the counterparty insists on some consolidation mechanism, accept a provision requiring the consent of all claimants and all respondents across all proceedings proposed to be consolidated, plus approval by the applicable tribunal(s).

**Rationale:**

> • Involuntary consolidation can expose Whitmore (or its fund vehicles) to procedural complexity, delay, and potential prejudice from having unrelated or tangentially related claims merged into a single proceeding.
>
> • Consolidation should be a consensual process reflecting the agreement of all affected parties.
>
> • In co-investment contexts, there may be related proceedings involving the target company, lenders (e.g., Claremont National Bank or other senior creditors), minority investors, or other co-investors, and Whitmore must retain control over whether those proceedings are merged with its own.

**[Section 12: Joinder of Third Parties]{.underline}**

**Required:** Joinder of any third party to the arbitration must require the **consent of all existing parties** to the arbitration **and** the **consent of the third party** to be joined. Both conditions must be satisfied.

**NOT ACCEPTABLE:** Joinder at the tribunal\'s discretion without the unanimous consent of all parties. Involuntary joinder undermines party autonomy --- a foundational principle of arbitration --- and may raise due process concerns that jeopardize the enforceability of the award.

**Preferred:** Same as Required. Additionally, any joined party must agree in writing to be bound by the arbitration agreement and all procedural orders previously issued by the tribunal.

**Fallback:** None --- unanimous consent for joinder is non-negotiable.

**Rationale:**

> • Arbitration is fundamentally a consensual process. Joining third parties without their consent (or without the consent of existing parties) raises due process concerns and may render the resulting award unenforceable under the Federal Arbitration Act.
>
> • In the co-investment context, potential third parties could include portfolio company management, lenders, co-investors in other fund vehicles, financial advisors, or other transaction participants. Whitmore must retain control over who participates in the proceeding, what claims are adjudicated, and what information is disclosed to third-party participants.

**[Section 13: Damages Limitations]{.underline}**

**Required:** The arbitration agreement must include an express **mutual waiver of punitive damages, exemplary damages, and consequential damages** --- including but not limited to lost profits, lost opportunities, diminution in value of other investments, and reputational harm.

**Required Carve-Out:** The damages waiver does **not** apply in cases of **fraud** or **willful misconduct**. In such cases, the tribunal may award any damages available under applicable law, including punitive and consequential damages where permitted by the governing law.

**Preferred:** The damages limitation should be mutual and should apply to all claims arising under the arbitration agreement and the underlying co-investment agreement, regardless of the legal theory (contract, tort, equity, or otherwise).

**Fallback:** If the counterparty resists a full consequential damages waiver, Whitmore will accept a waiver of punitive and exemplary damages only (with the fraud/willful misconduct carve-out preserved). Outside counsel must escalate to the General Counsel before accepting a narrower damages limitation.

**Rationale:**

> • Uncapped damages exposure --- particularly punitive and consequential damages --- creates disproportionate risk in high-value co-investment transactions. A \$325 million equity investment could theoretically give rise to multi-billion-dollar consequential damages claims based on lost profits, lost deal opportunities, or portfolio-wide impact.
>
[ACTION] Bash {"command": "sed -n 280,551p /tmp/playbook.txt", "description": "Read playbook second half"}
[OBSERVATION]
>
> • The mutual waiver allocates this risk symmetrically and is consistent with market practice in private equity co-investment agreements.
>
> • The fraud/willful misconduct carve-out preserves accountability for genuinely egregious conduct and ensures that the damages limitation cannot be used as a shield for bad-faith behavior.

**[Section 14: Fees and Costs]{.underline}**

**Required:** The arbitration agreement must include a **prevailing-party fee-shifting provision** under which the substantially prevailing party is entitled to recover its **reasonable attorneys\' fees, expert witness fees, arbitrator fees, administrative fees, and other costs** of the arbitration from the non-prevailing party.

**Preferred:** The tribunal determines which party is the \"substantially prevailing party\" and the reasonableness of claimed fees and costs in the final award.

**Fallback:** If the counterparty objects to full fee-shifting, accept a provision granting the tribunal discretion to allocate fees and costs based on the relative success of the parties\' respective claims and defenses.

**NOT ACCEPTABLE:** A provision under which each party bears its own attorneys\' fees and costs regardless of outcome. Such a provision incentivizes frivolous claims and tactical arbitration filings because there is no cost consequence for the losing party.

**Rationale:**

> • Fee-shifting deters frivolous or tactical claims.
>
> • Fee-shifting ensures the prevailing party is made whole --- or closer to whole --- by recovering the costs of vindicating its rights.
>
> • Fee-shifting aligns the economic incentives of both parties with the merits of their respective positions, promoting good-faith engagement in the arbitral process.

**[Section 15: Statute of Limitations]{.underline}**

**Required:** The arbitration agreement must **not** shorten the applicable statute of limitations below the statutory period under the governing substantive law. The contractual limitations period must **track** the statutory period.

**Required Minimum:** In no event shall the limitations period for contract-based claims be shorter than **three (3) years** from the date the claim accrues.

**Reference:** Under Delaware law (Whitmore\'s preferred governing law), the statute of limitations for breach of contract claims not under seal is **three (3) years** (10 Del. C. § 8106). Under New York law (Whitmore\'s fallback governing law), the statute of limitations for breach of contract claims is **six (6) years** (N.Y. C.P.L.R. § 213).

**NOT ACCEPTABLE:** Any contractual shortening of the statute of limitations below the applicable statutory period. Shortened limitations periods may be unenforceable in certain jurisdictions, create traps for the unwary, and may bar legitimate claims before a party has had an adequate opportunity to discover the relevant facts giving rise to the claim.

**Preferred:** Silent on limitations --- that is, let the statutory limitations period apply by default under the governing law without any contractual modification.

**Fallback:** If the counterparty insists on including a contractual limitations period, it must be no shorter than the longer of (a) the applicable statutory period and (b) three (3) years.

**Rationale:**

> • Private equity disputes --- particularly those involving valuation, earnout, governance, or fiduciary duty matters --- often do not fully manifest until well after the triggering event. Delayed discovery of breaches is common in contexts involving complex financial reporting, quarterly and annual audit cycles, and multi-year investment horizons.
>
> • A **one (1) year** limitations period --- commonly proposed by counterparties --- is particularly dangerous because fund operations involve quarterly and annual reporting cycles that may not reveal breaches or losses within twelve (12) months of the triggering event. By the time a breach is identified through the normal course of fund reporting and audit, a one-year limitations period may have already expired.
>
> • The three-year minimum floor is set at the Delaware statutory period, which is the shortest limitations period applicable under any of Whitmore\'s preferred governing law options.

**[Section 16: Class, Collective, and Representative Action Waiver]{.underline}**

**Required:** The arbitration agreement must include an **express waiver** of the right to participate in or bring **class actions, collective actions, or representative proceedings** of any kind. All disputes must be arbitrated on an **individual basis** between the named parties to the agreement.

**Required Language** (or substantially equivalent):

> *\"The parties agree that any arbitration under this Agreement shall be conducted on an individual basis only. No party may bring or participate in any class, collective, consolidated, or representative proceeding in arbitration or in any court. The arbitral tribunal shall have no authority to preside over any form of class, collective, or representative proceeding.\"*

**Preferred:** Same as Required.

**Fallback:** None --- this is non-negotiable.

**Rationale:**

> • Class or representative arbitration vastly increases Whitmore\'s exposure and introduces procedural complexity that is inconsistent with the bilateral nature of co-investment agreements.
>
> • In the private equity co-investment context, the risk is that minority investors, co-investors in parallel vehicles, or other stakeholders could attempt to aggregate claims against Whitmore or a Whitmore-managed fund vehicle.
>
> • An express waiver eliminates this risk and ensures that each dispute is resolved on its own facts between the parties to the specific agreement.

**[Section 17: Expedited Procedures for Critical Disputes]{.underline}**

**Required:** The arbitration agreement must include an **expedited dispute resolution track** for disputes involving any of the following subject matters:

> 1\. **Capital call disputes** --- including disputes regarding the timing, amount, validity, or enforceability of capital calls.
>
> 2\. **Drag-along rights** --- including disputes regarding the exercise, conditions, pricing, or procedural requirements of drag-along provisions.
>
> 3\. **Buy-sell provisions** --- including disputes regarding the triggering, valuation, mechanics, or timing of buy-sell (shotgun) clauses.

**Required Expedited Procedure Terms:**

> • **Sole arbitrator** (notwithstanding the three-member panel requirement for general disputes under Section 4).
>
> • **Arbitrator appointment within ten (10) business days** of the filing of the demand for arbitration.
>
> • **Hearing to be conducted within thirty (30) days** of the arbitrator\'s appointment.
>
> • **Final award to be rendered within forty-five (45) days** of the filing of the demand for arbitration.
>
> • **Limited discovery:** Document production only (no depositions); maximum of five (5) document requests per side.

**Preferred:** Same as Required.

**Fallback:** If the counterparty objects to the 45-day timeline, accept up to **sixty (60) days**, but not longer.

**Rationale:**

> • Capital call, drag-along, and buy-sell disputes have time-sensitive commercial consequences that cannot tolerate standard arbitration timelines.
>
> • A delayed or disputed capital call can jeopardize a transaction closing or trigger default provisions under the fund\'s limited partnership agreement.
>
> • A disputed drag-along can prevent or delay a sale transaction, causing the window for an exit to close.
>
> • A buy-sell dispute can freeze governance and create operational paralysis within the portfolio company.
>
> • Standard arbitration timelines (90+ days to hearing, plus additional time for post-hearing briefing and award) are inadequate for these time-critical contexts.
>
> • **Rebecca Stadler has specifically identified expedited procedures for capital call and drag-along disputes as \"critical for fund governance\" in the current Vantage Specialty Chemicals Inc. transaction.**

**[Section 18: Arbitral Award --- Timeline and Content]{.underline}**

**Required:** The arbitral tribunal must issue its final award within **ninety (90) days** of the close of proceedings --- defined as the date on which the last post-hearing submission is filed or the hearing transcript is received by the tribunal, whichever is later.

**Required:** The award must include both of the following:

> 1\. **Findings of fact** --- a detailed statement of the factual determinations underlying the award.
>
> 2\. **Conclusions of law** --- a detailed statement of the legal analysis and reasoning applied to those facts.

A \"reasoned award\" that does not include both specific findings of fact and specific conclusions of law is insufficient to satisfy this requirement.

**Preferred:** Same as Required.

**Fallback:** If the counterparty objects to the 90-day timeline, accept up to **one hundred twenty (120) days**, but findings of fact and conclusions of law are **non-negotiable** and must be included regardless of timeline.

**Rationale:**

> • A 90-day timeline is consistent with market practice for commercial arbitration of this complexity and provides the tribunal adequate time to deliberate and draft a thorough award.
>
> • Findings of fact and conclusions of law are necessary to: (a) enable meaningful review of the award, including for manifest disregard of the law under the Federal Arbitration Act; (b) provide a sufficient record for any appellate arbitration (*see* Section 19); and (c) ensure the tribunal has rigorously analyzed the dispute rather than issuing a summary disposition.

**[Section 19: Appellate Arbitration]{.underline}**

**Required:** For any award (or series of awards in a single proceeding) that exceeds **\$25 million** in aggregate monetary relief --- including damages, interest, fees, and costs --- the arbitration agreement must provide for **optional appellate arbitration**.

**Required Mechanism:** The appellate arbitration shall be conducted under the **AAA Optional Appellate Arbitration Rules** or, if the administering institution is JAMS, the JAMS equivalent appellate rules.

**Required Terms:**

> • Either party may elect to appeal the award by filing a notice of appeal within **thirty (30) days** of the issuance of the award.
>
> • The appellate panel shall consist of **three (3) arbitrators** drawn from the administering institution\'s appellate roster.
>
> • The standard of review shall be as set forth in the applicable appellate arbitration rules (generally, errors of law that are material and prejudicial, and findings of fact that are clearly erroneous).
>
> • The award shall not become final and enforceable until the appeal period has expired without a notice of appeal being filed, or the appellate panel has issued its decision on the appeal.

**Preferred:** Same as Required.

**Fallback:** If the counterparty objects to mandatory appellate arbitration provisions, accept a provision that the parties may agree post-award to submit the award to appellate arbitration by mutual written consent.

**Rationale:**

> • A \$25 million or greater award in a co-investment dispute could have fund-level implications, including material effects on fund returns, reserves, and LP distributions.
>
> • The finality of arbitration, while generally an advantage, creates unacceptable risk at this magnitude without a check against material legal error.
>
> • The AAA Optional Appellate Arbitration Rules provide a structured, efficient review mechanism that preserves the efficiency benefits of arbitration while protecting against erroneous awards of significant magnitude.

**[Section 20: Document Retention]{.underline}**

**Required:** The arbitration agreement must **NOT** require the destruction of documents or materials produced during the arbitration. Any mandatory destruction clause must be **deleted** from the counterparty\'s proposed agreement.

**Required:** All documents, materials, submissions, transcripts, evidence, and awards from the arbitration must be **retained for a minimum of seven (7) years** following the issuance of the final award (or the final appellate award, if appellate arbitration is invoked under Section 19).

**NOT ACCEPTABLE:** Any provision requiring destruction of arbitration documents within any time period after the issuance of the award. This is a categorical prohibition. Provisions requiring destruction within 30, 60, 90, or any other number of days are equally unacceptable.

**Rationale:**

> • Whitmore\'s fund document retention policies require a minimum seven (7) year retention period for all material fund records, including dispute-related records.
>
> • Premature destruction may compromise the ability to enforce or defend against vacatur of the award in subsequent court proceedings.
>
> • Premature destruction may compromise appellate arbitration rights under Section 19 if the relevant materials are no longer available.
>
> • Tax and regulatory audit cycles may require access to arbitration records for years after the issuance of the award.
>
> • LP reporting obligations and fiduciary duties may require reference to arbitration records during the life of the fund and any applicable wind-down period.

**Preferred:** Same as Required.

**Fallback:** If the counterparty insists on some document management provision, accept a provision requiring the **return** (not destruction) of produced documents to the producing party, with retention of all other materials --- including submissions, transcripts, orders, and awards --- for a minimum of seven (7) years.

**[Section 21: Language of Arbitration]{.underline}**

**Required:** The language of the arbitration must be **English** for all domestic U.S. transactions. This is standard and non-controversial.

**[Section 22: General Negotiation Instructions]{.underline}**

Outside counsel must review every counterparty-proposed arbitration agreement against each section of this playbook. The following priority classifications govern the order and intensity of negotiation:

**Critical (Non-Negotiable):**

> • Preservation of interim and emergency court relief (Section 10)
>
> • Arbitrator panel composition for disputes over \$10M (Section 4)
>
> • Governing law --- Delaware or New York only (Section 6)
>
> • Statute of limitations --- no shortening below statutory period / 3-year minimum (Section 15)
>
> • Class, collective, and representative action waiver (Section 16)

**Important (Strongly Preferred):**

> • Administering institution --- AAA, not ICC for domestic transactions (Section 2)
>
> • Seat of arbitration --- Atlanta, or New York as fallback (Section 3)
>
> • Confidentiality provision --- must be present and comprehensive (Section 9)
>
> • Damages limitation --- waiver of punitive and consequential damages (Section 13)
>
> • Fee-shifting --- prevailing-party recovery (Section 14)
>
> • Joinder and consolidation --- unanimous consent required (Sections 11--12)
>
> • Document retention --- no destruction, 7-year minimum retention (Section 20)
>
> • Appellate arbitration mechanism for awards over \$25M (Section 19)

**Recommended:**

> • Arbitrator qualifications --- 15 years PE/M&A experience (Section 5)
>
> • Discovery limitations --- specific caps on depositions, document requests, experts (Section 8)
>
> • Award timeline and content --- 90 days, findings of fact and conclusions of law (Section 18)
>
> • Expedited procedures for capital call, drag-along, and buy-sell disputes (Section 17)

**Markup Protocol:** If a counterparty\'s proposed agreement departs from a \"Required\" position, outside counsel must flag the departure in the redline markup with a comment referencing the specific playbook section number and indicating the position classification (Required, Preferred, or Fallback).

**Escalation Protocol:** If the counterparty is unwilling to accept a Required position after good-faith negotiation, outside counsel must escalate to the General Counsel (Rebecca Stadler) before conceding or accepting any compromise.

**Current Transaction Note:** For the current Vantage Specialty Chemicals Inc. / Cascadian Growth Fund LP co-investment, the markup deadline is **January 13, 2025**. All markup submissions must be strictly on time.

**[Section 23: Approved Sample Language]{.underline}**

Whitmore maintains a library of approved sample arbitration clauses, available upon request from the General Counsel\'s office. Outside counsel should use the sample language as a starting point for any new drafting and should reference the sample clauses when inserting provisions that are absent from a counterparty\'s proposed agreement.

The following provisions may need to be drafted and inserted from scratch if they are absent from the counterparty\'s form:

> • Confidentiality provision (Section 9)
>
> • Damages limitation and waiver (Section 13)
>
> • Class, collective, and representative action waiver (Section 16)
>
> • Expedited procedures for capital call, drag-along, and buy-sell disputes (Section 17)
>
> • Appellate arbitration mechanism (Section 19)

Outside counsel should contact the General Counsel\'s office to obtain the current approved forms of these provisions.

**[Section 24: Version History and Contact Information]{.underline}**

**Version History:**

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Version**             **Date**                **Description**
  ----------------------- ----------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  3.0                     November 15, 2024       Current version. Added appellate arbitration section (Section 19), expedited procedures section (Section 17), and revised arbitrator qualification requirements (Section 5). Updated negotiation priority classifications.

  2.0                     March 2022              Initial comprehensive update.

  1.0                     September 2019          Original version.
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Contact:**

Rebecca Stadler, General Counsel Whitmore Capital Partners LLC 3400 Peachtree Road NE, Suite 1200 Atlanta, GA 30326

**Distribution Notice:** This playbook is distributed on a confidential basis to approved outside counsel firms only. It is protected by the attorney-client privilege and the work product doctrine. Current distribution list includes Hargrove, Wynn & Calloway LLP (David Ostrander, Partner; Priya Nakamura, Associate). Do not copy or distribute without the prior written consent of the General Counsel.

**END OF DOCUMENT** PRIVILEGED & CONFIDENTIAL --- ATTORNEY-CLIENT PRIVILEGED / WORK PRODUCT
[ACTION] Bash {"command": "cd /tmp && rm -rf agx && mkdir agx && cd agx && unzip -q ./documents/proposed-arbitration-agreement.docx && find . -type f && wc -c word/document.xml && python3 -c \"import lxml; print('lxml', lxml.__version__)\"; pandoc --version | head -1; python3 -c \"\nimport re\nx=open('word/document.xml',encoding='utf8').read()\nps=re.findall(r'<w:p[ >].*?</w:p>',x,flags=re.S)\nprint(len(ps))\nfor i,p in enumerate(ps[:12]): print(i, p[:600].replace('\\n',' '),'\\n')\n\"", "description": "Unzip agreement and inspect XML structure"}
[OBSERVATION]
./[Content_Types].xml
./docProps/app.xml
./docProps/thumbnail.jpeg
./docProps/core.xml
./customXml/item1.xml
./customXml/_rels/item1.xml.rels
./customXml/itemProps1.xml
./_rels/.rels
./word/fontTable.xml
./word/document.xml
./word/header1.xml
./word/settings.xml
./word/numbering.xml
./word/footer1.xml
./word/webSettings.xml
./word/styles.xml
./word/theme/theme1.xml
./word/_rels/document.xml.rels
./word/stylesWithEffects.xml
   61226 word/document.xml
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import lxml; print('lxml', lxml.__version__)
    ^^^^^^^^^^^
ModuleNotFoundError: No module named 'lxml'. Did you mean: 'xml'?
pandoc 3.12.1
85
0 <w:p><w:pPr><w:spacing w:line="276" w:lineRule="auto" w:before="0" w:after="120"/><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>EXHIBIT F TO CO-INVESTMENT AGREEMENT</w:t></w:r></w:p> 

1 <w:p><w:pPr><w:spacing w:line="276" w:lineRule="auto" w:before="0" w:after="120"/><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>ARBITRATION AGREEMENT</w:t></w:r></w:p> 

2 <w:p><w:pPr><w:spacing w:line="276" w:lineRule="auto" w:before="0" w:after="120"/><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>Dated as of January 15, 2025</w:t></w:r></w:p> 

3 <w:p><w:pPr><w:spacing w:line="276" w:lineRule="auto" w:before="0" w:after="120"/><w:jc w:val="both"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>This Arbitration Agreement (this "</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>Agreement</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>") is entered into as of 

4 <w:p><w:pPr><w:keepNext/><w:spacing w:line="276" w:lineRule="auto" w:before="360" w:after="120"/><w:jc w:val="left"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:color w:val="000000"/><w:sz w:val="22"/><w:u w:val="single"/></w:rPr><w:t>RECITALS</w:t></w:r></w:p> 

5 <w:p><w:pPr><w:spacing w:line="276" w:lineRule="auto" w:before="0" w:after="120"/><w:jc w:val="both"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>WHEREAS</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>, Whitmore Capital Fund III LP, a Delaware limited partnership ("</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:color w:val="000000"/><w:sz w:val="22"/></ 

6 <w:p><w:pPr><w:spacing w:line="276" w:lineRule="auto" w:before="0" w:after="120"/><w:jc w:val="both"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>WHEREAS</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>, pursuant to the Co-Investment Agreement, the Parties have agreed to jointly acquire a controlling interest (approximately 72%) of Vantage Specialty Chemicals Inc., a Delaware corporation headquartered  

7 <w:p><w:pPr><w:spacing w:line="276" w:lineRule="auto" w:before="0" w:after="120"/><w:jc w:val="both"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>WHEREAS</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>, the Co-Investment Agreement governs, among other things, governance rights, drag-along and tag-along rights, transfer restrictions, and capital call mechanics relating to the Parties' investment in the 

8 <w:p><w:pPr><w:spacing w:line="276" w:lineRule="auto" w:before="0" w:after="120"/><w:jc w:val="both"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>WHEREAS</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>, the Parties desire to establish the terms and procedures by which disputes arising under or in connection with the Co-Investment Agreement shall be resolved.</w:t></w:r></w:p> 

9 <w:p><w:pPr><w:spacing w:line="276" w:lineRule="auto" w:before="0" w:after="120"/><w:jc w:val="both"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>NOW, THEREFORE</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="000000"/><w:sz w:val="22"/></w:rPr><w:t>, in consideration of the mutual covenants and agreements set forth in the Co-Investment Agreement, and for other good and valuable consideration, the receipt and sufficiency of which are hereby a 

10 <w:p><w:r><w:br w:type="page"/></w:r></w:p> 

11 <w:p><w:pPr><w:keepNext/><w:spacing w:line="276" w:lineRule="auto" w:before="360" w:after="120"/><w:jc w:val="left"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:color w:val="000000"/><w:sz w:val="22"/><w:u w:val="single"/></w:rPr><w:t>ARTICLE I — DEFINITIONS</w:t></w:r></w:p>
Shell cwd was reset to .
[ACTION] Bash {"command": "cd /tmp && python3 -m pip install -q lxml 2>&1 | tail -2; python3 -c \"import lxml; print('ok', lxml.__version__)\"; cd /tmp/agx && grep -o '<w:r>' word/document.xml | wc -l; grep -c 'w:tab\\|w:br' word/document.xml; grep -o '<w:r [^>]*>' word/document.xml | sort | uniq -c | head; head -c 900 word/document.xml; echo; cat word/_rels/document.xml.rels; echo; cat '[Content_Types].xml'", "description": "Install lxml and inspect run and rels structure"}
[OBSERVATION]
ERROR: Could not install packages due to an OSError: [Errno 1] Operation not permitted: '/Users/me/Library/Python/3.15'

Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import lxml; print('ok', lxml.__version__)
    ^^^^^^^^^^^
ModuleNotFoundError: No module named 'lxml'. Did you mean: 'xml'?
     237
1
<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" xmlns:mo="http://schemas.microsoft.com/office/mac/office/2008/main" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:mv="urn:schemas-microsoft-com:mac:vml" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:w14="http://schemas.microsoft.com/office/w
<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId4" Type="http://schemas.microsoft.com/office/2007/relationships/stylesWithEffects" Target="stylesWithEffects.xml"/><Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/><Relationship Id="rId6" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/webSettings" Target="webSettings.xml"/><Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable" Target="fontTable.xml"/><Relationship Id="rId8" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/customXml" Target="../customXml/item1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/><Relationship Id="rId9" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/><Relationship Id="rId10" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/></Relationships>
<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="jpeg" ContentType="image/jpeg"/><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/customXml/itemProps1.xml" ContentType="application/vnd.openxmlformats-officedocument.customXmlProperties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/><Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/><Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/><Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/stylesWithEffects.xml" ContentType="application/vnd.ms-word.stylesWithEffects+xml"/><Override PartName="/word/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/><Override PartName="/word/webSettings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.webSettings+xml"/></Types>
Shell cwd was reset to .
[ACTION] Bash {"command": "cd /tmp && python3 -m venv /tmp/venv && /tmp/venv/bin/pip install -q lxml python-docx 2>&1 | tail -2; /tmp/venv/bin/python -c \"import lxml, docx; print('ok')\"", "description": "Create venv and install lxml and python-docx"}
[OBSERVATION]
ok
Shell cwd was reset to .
[ACTION] Bash {"command": "cd /tmp/agx && /tmp/venv/bin/python -c \"\nfrom lxml import etree\nW='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'\nt=etree.parse('word/document.xml')\nbody=t.getroot().find(W+'body')\nfor i,p in enumerate(body.iter(W+'p')):\n    txt=''.join(x.text or '' for x in p.iter(W+'t'))\n    print(i, len(list(p.iter(W+'r'))), txt[:110])\n\"", "description": "List paragraphs with indices and text"}
[OBSERVATION]
0 1 EXHIBIT F TO CO-INVESTMENT AGREEMENT
1 1 ARBITRATION AGREEMENT
2 1 Dated as of January 15, 2025
3 5 This Arbitration Agreement (this "Agreement") is entered into as of January 15, 2025, by and between the follo
4 1 RECITALS
5 12 WHEREAS, Whitmore Capital Fund III LP, a Delaware limited partnership ("Whitmore"), an investment vehicle mana
6 6 WHEREAS, pursuant to the Co-Investment Agreement, the Parties have agreed to jointly acquire a controlling int
7 2 WHEREAS, the Co-Investment Agreement governs, among other things, governance rights, drag-along and tag-along 
8 2 WHEREAS, the Parties desire to establish the terms and procedures by which disputes arising under or in connec
9 2 NOW, THEREFORE, in consideration of the mutual covenants and agreements set forth in the Co-Investment Agreeme
10 1 
11 1 ARTICLE I — DEFINITIONS
12 1 As used in this Agreement, the following terms shall have the meanings set forth below:
13 3 "Agreement" means this Arbitration Agreement, as it may be amended from time to time in accordance with its te
14 5 "Arbitral Tribunal" or "Tribunal" means the arbitrator or arbitrators appointed pursuant to Article IV of this
15 3 "Award" means any interim, partial, or final award rendered by the Arbitral Tribunal in connection with any Pr
16 3 "Claimant" means the Party initiating a Proceeding by filing a request for arbitration.
17 5 "Co-Investment Agreement" or "CIA" has the meaning set forth in the Recitals.
18 3 "Company" means Vantage Specialty Chemicals Inc., a Delaware corporation.
19 3 "Dispute" means any dispute, controversy, or claim arising out of, relating to, or in connection with this Agr
20 3 "ICC" means the International Chamber of Commerce.
21 3 "ICC Rules" means the Rules of Arbitration of the International Chamber of Commerce in effect at the time of c
22 5 "Party" and "Parties" have the meanings set forth in the Recitals.
23 3 "Proceedings" means any arbitration proceedings commenced pursuant to this Agreement.
24 3 "Respondent" means the Party against whom a request for arbitration is filed.
25 3 "Seat" means Seattle, Washington, which shall be the juridical seat of any arbitration conducted under this Ag
26 1 ARTICLE II — AGREEMENT TO ARBITRATE; SCOPE
27 4 Section 2.1 — Agreement to Arbitrate. Any and all disputes, controversies, or claims arising out of, relating 
28 2 Section 2.2 — Exclusive Remedy. Arbitration under this Agreement shall be the exclusive remedy for any Dispute
29 1 ARTICLE III — SEAT, LANGUAGE, AND GOVERNING LAW
30 2 Section 3.1 — Seat of Arbitration. The seat (legal place) of arbitration shall be Seattle, Washington. Any hea
31 2 Section 3.2 — Language. The language of the arbitration shall be English. All submissions, correspondence, evi
32 2 Section 3.3 — Governing Law. This Agreement shall be governed by and construed in accordance with the laws of 
33 1 
34 1 ARTICLE IV — ARBITRATOR APPOINTMENT AND QUALIFICATIONS
35 4 Section 4.1 — Number of Arbitrators. The arbitration shall be conducted by a sole arbitrator (the "Arbitrator"
36 2 Section 4.2 — Appointment Procedure. The Parties shall endeavor to agree upon a mutually acceptable Arbitrator
37 2 Section 4.3 — Qualifications. The Arbitrator shall be a neutral individual independent of the Parties.
38 1 ARTICLE V — ARBITRATION PROCEDURES
39 2 Section 5.1 — Discovery. Discovery shall be conducted in accordance with the ICC Rules, without modification. 
40 2 Section 5.2 — Hearings. The Arbitrator shall hold hearings as the Arbitrator deems necessary and appropriate. 
41 2 Section 5.3 — Evidence. The Arbitrator shall have the authority to receive and consider such evidence as the A
42 1 ARTICLE VI — INTERIM AND EMERGENCY RELIEF
43 2 Section 6.1 — Waiver of Court Relief. The Parties hereby expressly waive any right to seek provisional or inte
44 1 
45 1 ARTICLE VII — CONSOLIDATION AND JOINDER
46 2 Section 7.1 — Consolidation. The Tribunal may, at the request of either Party, consolidate this arbitration wi
47 2 Section 7.2 — Joinder of Third Parties. Third parties may be joined to the arbitration at the discretion of th
48 1 ARTICLE VIII — AWARD
49 2 Section 8.1 — Timing and Form of Award. The Arbitrator shall use best efforts to issue a reasoned award within
50 2 Section 8.2 — Finality. The award of the Arbitrator shall be final and binding upon the Parties and shall not 
51 2 Section 8.3 — Remedies. The Arbitrator shall have the authority to award any remedy or relief that a court of 
52 1 
53 1 ARTICLE IX — COSTS AND FEES
54 2 Section 9.1 — Allocation of Costs. Each Party shall bear its own costs and expenses of the arbitration, includ
55 2 Section 9.2 — Administrative Costs. The administrative fees and expenses of the ICC and the fees and expenses 
56 1 ARTICLE X — LIMITATIONS PERIOD
57 2 Section 10.1 — Statute of Limitations. All claims subject to arbitration under this Agreement must be commence
58 1 ARTICLE XI — DOCUMENT RETENTION AND DESTRUCTION
59 2 Section 11.1 — Post-Arbitration Document Handling. The Parties agree that, within thirty (30) days following t
60 1 
61 1 ARTICLE XII — GENERAL PROVISIONS
62 2 Section 12.1 — Notices. All notices, requests, demands, and other communications under this Agreement shall be
63 2 Section 12.2 — Entire Agreement. This Agreement constitutes the entire agreement between the Parties with resp
64 2 Section 12.3 — Amendment and Waiver. This Agreement may not be amended, modified, or supplemented except by a 
65 2 Section 12.4 — Severability. If any provision of this Agreement is held to be invalid, illegal, or unenforceab
66 2 Section 12.5 — Counterparts. This Agreement may be executed in counterparts, each of which shall be deemed an 
67 2 Section 12.6 — Relationship to Co-Investment Agreement. This Agreement is Exhibit F to and is incorporated int
68 2 Section 12.7 — Survival. This Agreement shall survive the termination or expiration of the Co-Investment Agree
69 1 
70 1 [Signature Page Follows]
71 1 
72 2 IN WITNESS WHEREOF, the Parties have executed this Arbitration Agreement as of the date first written above.
73 1 WHITMORE CAPITAL FUND III LP
74 1 By: Whitmore Capital Partners LLC, its General Partner
75 9 By: ________
76 9 Name: ________
77 9 Title: ________
78 9 Date: ________
79 1 CASCADIAN GROWTH FUND LP
80 1 By: Cascadian Growth Management LLC, its General Partner
81 9 By: ________
82 9 Name: ________
83 9 Title: ________
84 9 Date: ________
Shell cwd was reset to .
[ASSISTANT] Read everything I need. Next I'll build the redline by editing the original docx XML directly so the changes are real tracked revisions, with comments.
[ACTION] Bash {"command": "mkdir -p /tmp/redline && cat > /tmp/redline/track.py <<'EOF'\n\"\"\"Tracked-change and comment helpers for a WordprocessingML document.xml (lxml).\"\"\"\nimport copy\nfrom lxml import etree\n\nW_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'\nW = '{%s}' % W_NS\nXML_SPACE = '{http://www.w3.org/XML/1998/namespace}space'\nAUTHOR = 'HWC Draft'\nINITIALS = 'HWC'\n\n\nclass Tracker:\n    def __init__(self, root):\n        self.root = root\n        self.rev_id = 1000\n        self.comments = []  # (id, [paragraph strings])\n\n    def _rid(self):\n        self.rev_id += 1\n        return str(self.rev_id)\n\n    # ---- text helpers -------------------------------------------------\n    @staticmethod\n    def run_text(r):\n        t = r.find(W + 't')\n        return (t.text or '') if t is not None else ''\n\n    def live_runs(self, p):\n        \"\"\"Direct-child runs with their [start, end) offsets in the live (not deleted) text.\"\"\"\n        out, pos = [], 0\n        for r in p:\n            if r.tag != W + 'r':\n                continue\n            s = self.run_text(r)\n            out.append((r, pos, pos + len(s)))\n            pos += len(s)\n        return out\n\n    def text(self, p):\n        return ''.join(self.run_text(r) for r, _, _ in self.live_runs(p))\n\n    def _split_at(self, p, pos):\n        for r, s, e in self.live_runs(p):\n            if s < pos < e:\n                txt = self.run_text(r)\n                r2 = copy.deepcopy(r)\n
[OBSERVATION]
done
[ACTION] Bash {"command": "cat > /tmp/redline/build_redline.py <<'EOF'\nimport sys, shutil, zipfile, os, copy\nsys.path.insert(0, '/tmp/redline')\nfrom lxml import etree\nfrom track import Tracker, W, W_NS\n\nSRC = '/tmp/agx'            # unzipped original\nOUT_DIR = '/tmp/redline/pkg'\nOUT_DOCX = sys.argv[1]\n\nif os.path.exists(OUT_DIR):\n    shutil.rmtree(OUT_DIR)\nshutil.copytree(SRC, OUT_DIR)\n\ndoc_path = os.path.join(OUT_DIR, 'word/document.xml')\ntree = etree.parse(doc_path)\nroot = tree.getroot()\nbody = root.find(W + 'body')\nP = list(body.iter(W + 'p'))   # original paragraph elements, indexed as in the audit listing\nT = Tracker(root)\n\ndef rpr_of(p, idx=-1):\n    runs = [r for r in p if r.tag == W + 'r' and r.find(W + 't') is not None]\n    r = runs[idx]\n    rp = r.find(W + 'rPr')\n    return copy.deepcopy(rp)\n\nBODY_T = P[36]     # plain body paragraph with bold heading run\nBODY_RPR = rpr_of(P[36], -1)\nHEAD_RPR = rpr_of(P[11], 0)   # bold + underlined article heading\nARTICLE_T = P[11]\n\n# ---------------- Internal draft banner (new first paragraph) ----------\nbanner = T.new_para_after(P[0].getprevious() if P[0].getprevious() is not None else P[0], P[2],\n    '**INTERNAL DRAFT - PRIVILEGED & CONFIDENTIAL - ATTORNEY WORK PRODUCT.** Hargrove, Wynn & Calloway draft markup for Whitmore Capital Partners review. Bracketed comments disclose Whitmore playbook positions and fallbacks; all comments must be removed before any version goes to Cascadian or Pinnacle Winterhaven.',\n
[OBSERVATION]
comments: 31 revisions up to id 1105
wrote /tmp/redline/out/redlined-arbitration-agreement.docx
Shell cwd was reset to .
[ASSISTANT] Built. Now verifying: reject-all must reproduce the original text, and accept-all must read cleanly.
[ACTION] Bash {"command": "cat > /tmp/redline/verify.py <<'EOF'\nimport sys, zipfile\nfrom lxml import etree\nW='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'\ndef load(path):\n    return etree.fromstring(zipfile.ZipFile(path).read('word/document.xml'))\ndef para_texts(root, mode):\n    out=[]\n    for p in root.iter(W+'p'):\n        mark = p.find(W+'pPr/'+W+'rPr/'+W+'ins')\n        mark_del = p.find(W+'pPr/'+W+'rPr/'+W+'del')\n        if mode=='reject' and mark is not None: continue\n        if mode=='accept' and mark_del is not None: continue\n        s=''\n        for el in p.iter():\n            anc=[a.tag for a in el.iterancestors()]\n            in_ins = W+'ins' in anc\n            in_del = W+'del' in anc\n            if el.tag==W+'t':\n                if mode=='reject' and in_ins: continue\n                s+=el.text or ''\n            elif el.tag==W+'delText':\n                if mode=='accept': continue\n                s+=el.text or ''\n        out.append(s)\n    return out\norig = load(sys.argv[1]); red = load(sys.argv[2])\no = para_texts(orig,'accept')\nr = para_texts(red,'reject')\nprint('original paras', len(o), 'reject-view paras', len(r), 'match:', o==r)\nif o!=r:\n    import difflib\n    for l in list(difflib.unified_diff(o,r,lineterm=''))[:30]: print(l[:200])\na = para_texts(red,'accept')\nopen('/tmp/redline/accepted.txt','w').write('\\n'.join(a))\nprint('accept-view paras', len(a))\nEOF\n/tmp/venv/bin/python /tmp/redline/verify.py /Users/me/
[OBSERVATION]
original paras 85 reject-view paras 85 match: True
accept-view paras 100
python-docx opens, paras 100
pandoc-ok
7:WHEREAS, Whitmore Capital Fund III LP, a Delaware limited partnership ("Whitmore"), an investment vehicle managed by Whitmore Capital Partners LLC, a Delaware limited liability company, with its principal office at 340
16:"Arbitral Tribunal" or "Tribunal" means the arbitrator or arbitrators appointed pursuant to Article IV of this Agreement to resolve a Dispute.
36:ARTICLE IV — ARBITRATOR APPOINTMENT AND QUALIFICATIONS
37:Section 4.1 — Number of Arbitrators. The arbitration shall be conducted by a three-member Tribunal, each member of which shall be an "Arbitrator" appointed in accordance with Section 4.2.
38:Section 4.2 — Appointment Procedure. Each Party shall appoint one Arbitrator within thirty (30) days after the filing of the demand for arbitration (where Parties are aligned as claimant or respondent, the aligned Par
39:Section 4.3 — Qualifications. Each Arbitrator shall be a neutral individual independent of the Parties who: (a) has at least fifteen (15) years of professional experience in private equity, mergers and acquisitions, o
45:Section 6.1 — Court Interim Relief; Emergency Arbitrator. Nothing in this Agreement shall preclude or restrict any Party from seeking provisional, interim, conservatory, or injunctive relief (including temporary restr
58:Section 9.1 — Allocation of Costs. The substantially prevailing Party shall be entitled to recover from the non-prevailing Party its reasonable attorneys' fees, expert witness fees, arbitrator fees, administrative fee
79:Section 14.2 - Sole Arbitrator; Appointment. An Expedited Dispute shall be heard by a sole Arbitrator meeting the qualifications in Section 4.3. The sole Arbitrator shall be appointed within ten (10) Business Days aft
80:Section 14.3 - Timetable. The hearing shall be conducted within thirty (30) days after the appointment of the sole Arbitrator, and the Expedited Award shall be rendered within forty-five (45) days after the filing of
[ASSISTANT] Reject-all matches the original exactly. Fixing one style issue (I typed hyphens where the form uses em dashes), then rebuilding and reviewing the accept view.
[ACTION] Bash {"command": "cd /tmp/redline && sed -i \"s/        for i, part in enumerate(text.split('\\*\\*')):/        text = text.replace(' - ', ' \\\\\\\\u2014 ')\\n        for i, part in enumerate(text.split('**')):/\" track.py && grep -n \"u2014\\|enumerate(text\" track.py && /tmp/venv/bin/python build_redline.py /tmp/redline/out/redlined-arbitration-agreement.docx && /tmp/venv/bin/python verify.py ./documents/proposed-arbitration-agreement.docx out/redlined-arbitration-agreement.docx | head -3 && cat accepted.txt | cut -c1-400 | sed -n '1,4p;24,70p'", "description": "Fix dash style, rebuild, and review accepted text"}
[OBSERVATION]
Exit code 1
sed: 2: "track.py
": undefined label 'rack.py'
[ACTION] Bash {"command": "cd /tmp/redline && /tmp/venv/bin/python - <<'EOF'\nimport re\ns=open('/tmp/redline/track.py',encoding='utf8').read()\nold=\"        for i, part in enumerate(text.split('**')):\"\nassert s.count(old)==1\ns=s.replace(old,\"        text = text.replace(' - ', ' \u2014 ')\\n\"+old)\nopen('/tmp/redline/track.py','w',encoding='utf8').write(s)\nprint('patched')\nEOF\n/tmp/venv/bin/python build_redline.py /tmp/redline/out/redlined-arbitration-agreement.docx && /tmp/venv/bin/python verify.py ./documents/proposed-arbitration-agreement.docx out/redlined-arbitration-agreement.docx | head -2; cut -c1-260 accepted.txt | sed -n '1,3p;24,60p'", "description": "Patch dash style, rebuild, verify, and review accept text"}
[OBSERVATION]
patched
comments: 31 revisions up to id 1105
wrote /tmp/redline/out/redlined-arbitration-agreement.docx
original paras 85 reject-view paras 85 match: True
accept-view paras 100
INTERNAL DRAFT — PRIVILEGED & CONFIDENTIAL — ATTORNEY WORK PRODUCT. Hargrove, Wynn & Calloway draft markup for Whitmore Capital Partners review. Bracketed comments disclose Whitmore playbook positions and fallbacks; all comments must be removed before any vers
EXHIBIT F TO CO-INVESTMENT AGREEMENT
ARBITRATION AGREEMENT
"Party" and "Parties" have the meanings set forth in the Recitals.
"Proceedings" means any arbitration proceedings commenced pursuant to this Agreement.
"Respondent" means the Party against whom a demand for arbitration is filed.
"Seat" means Atlanta, Georgia, which shall be the juridical seat of any arbitration conducted under this Agreement.
ARTICLE II — AGREEMENT TO ARBITRATE; SCOPE
Section 2.1 — Agreement to Arbitrate. Any and all disputes, controversies, or claims arising out of, relating to, or in connection with this Agreement or the Co-Investment Agreement, including but not limited to the formation, validity, interpretation, perform
Section 2.2 — Exclusive Remedy. Arbitration under this Agreement shall be the exclusive remedy for any Dispute, and no Party shall institute any action or proceeding in any court with respect to any Dispute, except (a) as provided in Section 6.1, (b) to compel
ARTICLE III — SEAT, LANGUAGE, AND GOVERNING LAW
Section 3.1 — Seat of Arbitration. The seat (legal place) of arbitration shall be Atlanta, Georgia. Any hearings shall be conducted at the Seat unless otherwise agreed by the Parties or ordered by the Arbitral Tribunal.
Section 3.2 — Language. The language of the arbitration shall be English. All submissions, correspondence, evidence, and hearings shall be conducted in English.
Section 3.3 — Governing Law. This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to its conflict of laws principles.

ARTICLE IV — ARBITRATOR APPOINTMENT AND QUALIFICATIONS
Section 4.1 — Number of Arbitrators. The arbitration shall be conducted by a three-member Tribunal, each member of which shall be an "Arbitrator" appointed in accordance with Section 4.2.
Section 4.2 — Appointment Procedure. Each Party shall appoint one Arbitrator within thirty (30) days after the filing of the demand for arbitration (where Parties are aligned as claimant or respondent, the aligned Parties shall jointly appoint one Arbitrator f
Section 4.3 — Qualifications. Each Arbitrator shall be a neutral individual independent of the Parties who: (a) has at least fifteen (15) years of professional experience in private equity, mergers and acquisitions, or corporate finance, including as an attorn
ARTICLE V — ARBITRATION PROCEDURES
Section 5.1 — Discovery. Discovery shall be conducted in accordance with the AAA Rules, subject to the following limits: each Party may (a) take up to three (3) fact depositions, each not to exceed seven (7) hours on the record; (b) serve up to fifteen (15) do
Section 5.2 — Hearings. The Tribunal shall hold hearings as the Tribunal deems necessary and appropriate. Hearings shall be held at the Seat unless otherwise agreed by the Parties or directed by the Tribunal.
Section 5.3 — Evidence. The Tribunal shall have the authority to receive and consider such evidence as the Tribunal deems relevant and material, including documentary evidence, witness testimony, and expert reports. The Tribunal shall determine the admissibili
ARTICLE VI — INTERIM AND EMERGENCY RELIEF
Section 6.1 — Court Interim Relief; Emergency Arbitrator. Nothing in this Agreement shall preclude or restrict any Party from seeking provisional, interim, conservatory, or injunctive relief (including temporary restraining orders, preliminary injunctions, att

ARTICLE VII — CONSOLIDATION AND JOINDER
Section 7.1 — Consolidation. No arbitration under this Agreement shall be consolidated with any other arbitration arising out of or in connection with the Co-Investment Agreement or any other agreement between the Parties or involving a Party to this Agreement
Section 7.2 — Joinder of Third Parties. No third party may be joined to any arbitration under this Agreement without the prior written consent of all Parties to the arbitration and of the third party to be joined. Any joined party shall agree in writing to be 
ARTICLE VIII — AWARD
Section 8.1 — Timing and Form of Award. Subject to Article XIV for Expedited Disputes, the Tribunal shall issue its final Award within ninety (90) days of the close of Proceedings, being the later of the filing of the last post-hearing submission and the Tribu
Section 8.2 — Finality. Subject to Section 8.4, the Award of the Tribunal shall be final and binding upon the Parties. Judgment upon the Award may be entered in any court of competent jurisdiction. Nothing in this Section 8.2 limits either Party's right to cha
Section 8.3 — Remedies. The Tribunal shall have the authority to award any remedy or relief that a court of competent jurisdiction could grant, including but not limited to specific performance, injunctive relief, and monetary damages. The Tribunal's authority
Section 8.4 — Optional Appellate Arbitration. For any Award (or series of Awards in a single proceeding) that exceeds Twenty-Five Million Dollars ($25,000,000) in aggregate monetary relief, including damages, interest, fees, and costs, either Party may elect t
Section 8.5 — Damages Limitation. Each Party waives, to the fullest extent permitted by law, any right to recover from the other Party punitive, exemplary, or consequential damages, including lost profits, lost opportunities, diminution in value of other inves

ARTICLE IX — COSTS AND FEES
Section 9.1 — Allocation of Costs. The substantially prevailing Party shall be entitled to recover from the non-prevailing Party its reasonable attorneys' fees, expert witness fees, arbitrator fees, administrative fees, and other costs of the arbitration. The 
Section 9.2 — Administrative Costs. The administrative fees and expenses of the AAA and the fees and expenses of the Tribunal shall be advanced equally by the Parties, subject to reallocation under Section 9.1 in the final Award.
ARTICLE X — LIMITATIONS PERIOD
Shell cwd was reset to .
[ACTION] Bash {"command": "cd /tmp/redline && cut -c1-200 accepted.txt | sed -n '61,100p'; echo; grep -c \"\" accepted.txt; grep -n \"ICC\\|Seattle\\|Washington\" accepted.txt | cut -c1-120", "description": "Review remaining accepted text and residual references"}
[OBSERVATION]
Section 10.1 — Statute of Limitations. The statute of limitations applicable under the governing law specified in Section 3.3 shall apply to all claims subject to arbitration under this Agreement. Not
ARTICLE XI — DOCUMENT RETENTION
Section 11.1 — Post-Arbitration Document Retention. All documents, materials, evidence, submissions, transcripts, orders, Awards, and other records produced, created, or exchanged in any arbitration u

ARTICLE XII — GENERAL PROVISIONS
Section 12.1 — Notices. All notices, requests, demands, and other communications under this Agreement shall be delivered in the manner provided in Section 11.4 of the Co-Investment Agreement to the Pa
Section 12.2 — Entire Agreement. This Agreement constitutes the entire agreement between the Parties with respect to the subject matter hereof and supersedes all prior negotiations, representations, w
Section 12.3 — Amendment and Waiver. This Agreement may not be amended, modified, or supplemented except by a written instrument signed by both Parties. No waiver of any provision of this Agreement sh
Section 12.4 — Severability. If any provision of this Agreement is held to be invalid, illegal, or unenforceable in any respect, such invalidity, illegality, or unenforceability shall not affect any o
Section 12.5 — Counterparts. This Agreement may be executed in counterparts, each of which shall be deemed an original, and all of which together shall constitute one and the same instrument. Executio
Section 12.6 — Relationship to Co-Investment Agreement. This Agreement is Exhibit F to and is incorporated into the Co-Investment Agreement. In the event of a conflict between the terms of this Agreem
Section 12.7 — Survival. This Agreement shall survive the termination or expiration of the Co-Investment Agreement with respect to any Dispute arising prior to or upon such termination or expiration.
ARTICLE XIII — CONFIDENTIALITY
Section 13.1 — Confidentiality. The existence of any arbitration under this Agreement; all submissions, briefs, motions, and pleadings filed in it; all evidence, testimony, exhibits, and documents pro
Section 13.2 — Permitted Disclosures. A Party may disclose such information only: (a) as required by applicable law, regulation, or order of a court of competent jurisdiction, including SEC reporting 
Section 13.3 — Injunctive Relief. Any breach or threatened breach of this Article XIII may be addressed by injunctive relief, including emergency relief, under Section 6.1.
ARTICLE XIV — EXPEDITED PROCEDURES FOR CRITICAL DISPUTES
Section 14.1 — Covered Disputes. Any Dispute concerning (a) a capital call, including its timing, amount, validity, or enforceability; (b) the exercise, conditions, pricing, or procedural requirements
Section 14.2 — Sole Arbitrator; Appointment. An Expedited Dispute shall be heard by a sole Arbitrator meeting the qualifications in Section 4.3. The sole Arbitrator shall be appointed within ten (10) 
Section 14.3 — Timetable. The hearing shall be conducted within thirty (30) days after the appointment of the sole Arbitrator, and the Expedited Award shall be rendered within forty-five (45) days aft
Section 14.4 — Discovery. Discovery in an Expedited Dispute is limited to document production. No depositions shall be taken, and each Party may serve no more than five (5) document requests.
Section 14.5 — Appellate Review. Section 8.4 applies to an Expedited Award that meets the threshold in that Section. [Appellate timetable for Expedited Awards: open, see memo.]
ARTICLE XV — INDIVIDUAL PROCEEDINGS
Section 15.1 — Individual Basis. Except for consolidation consented to under Section 7.1, any arbitration under this Agreement shall be conducted on an individual basis only. No Party may bring or par

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
100
7:WHEREAS, Whitmore Capital Fund III LP, a Delaware limited partnership ("Whitmore"), an investment vehicle managed by W
Shell cwd was reset to .
[ASSISTANT] Redline checks pass: reject-all reproduces the original, accept-all reads cleanly, and the only remaining "Washington" is the recital's Cascadian address. Now the cover memo.
[ACTION] Bash {"command": "mkdir -p /tmp/redline/memo && cat > /tmp/redline/memo/build_memo.py <<'EOF'\nimport sys\nfrom docx import Document\nfrom docx.shared import Pt, Inches\nfrom docx.enum.text import WD_ALIGN_PARAGRAPH\nfrom docx.oxml.ns import qn\nfrom docx.oxml import OxmlElement\n\nOUT = sys.argv[1]\nd = Document()\nst = d.styles['Normal']\nst.font.name = 'Times New Roman'; st.font.size = Pt(10.5)\nst.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')\nfor s in d.sections:\n    s.left_margin = s.right_margin = Inches(0.8)\n    s.top_margin = s.bottom_margin = Inches(0.8)\n\ndef para(text, bold=False, italic=False, size=None, align=None, space_after=4):\n    p = d.add_paragraph()\n    r = p.add_run(text); r.bold = bold; r.italic = italic\n    if size: r.font.size = Pt(size)\n    if align: p.alignment = align\n    p.paragraph_format.space_after = Pt(space_after)\n    return p\n\ndef head(text):\n    p = d.add_paragraph()\n    r = p.add_run(text); r.bold = True; r.font.size = Pt(12)\n    p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(4)\n    p.paragraph_format.keep_with_next = True\n\ndef bullet(text):\n    p = d.add_paragraph(style='List Bullet')\n    p.add_run(text)\n    p.paragraph_format.space_after = Pt(2)\n\ndef shade(cell, hexcolor):\n    tcPr = cell._tc.get_or_add_tcPr()\n    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), hexcolor)\n    tcPr.append(sh)\n\ndef table(header, ro
[OBSERVATION]
wrote /tmp/redline/out/markup-cover-memo.docx
reopens; paras 52 tables 5
Shell cwd was reset to .
[ASSISTANT] Both files built and reopen. Copying them to the deliverable directory and running a final check.
[ACTION] Bash {"command": "W=.; cp /tmp/redline/out/redlined-arbitration-agreement.docx /tmp/redline/out/markup-cover-memo.docx \"$W/output/\" && cd \"$W\" && ls -la output && python3 scripts/read_doc.py output/markup-cover-memo.docx | head -c 1200 && echo && /tmp/venv/bin/python -c \"\nimport zipfile,re\nz=zipfile.ZipFile('output/redlined-arbitration-agreement.docx')\nd=z.read('word/document.xml').decode()\nprint('ins',len(re.findall(r'<w:ins ',d)),'del',len(re.findall(r'<w:del ',d)),'commentRef',len(re.findall(r'commentReference',d)))\nprint('comments.xml comments', z.read('word/comments.xml').decode().count('<w:comment '))\nprint(z.testzip())\"", "description": "Copy deliverables to output and final integrity check"}
[OBSERVATION]
total 200
drwxr-xr-x@ 4 me  staff    128 Oct 19 12:12 .
drwxr-xr-x@ 7 me  staff    224 Oct 19 12:01 ..
-rw-r--r--@ 1 me  staff  43794 Oct 19 12:12 markup-cover-memo.docx
-rw-r--r--@ 1 me  staff  54571 Oct 19 12:12 redlined-arbitration-agreement.docx
**PRIVILEGED & CONFIDENTIAL - ATTORNEY WORK PRODUCT - INTERNAL DRAFT**

**MEMORANDUM**

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **To:**                             David Ostrander, Partner (review first). After his review: Rebecca Stadler, General Counsel, Whitmore Capital Partners LLC.
  ----------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **From:**                           Hargrove, Wynn & Calloway LLP deal team (draft prepared for review by Priya Nakamura; not yet reviewed)

  **Date:**                           \[January 11, 2025\] - DRAFT

  **Re:**                             Vantage Specialty Chemicals / Cascadian co-investment - markup of Exhibit F (Arbitration Agreement) against the Whitmore Arbitration Playbook v3.0 (Nov. 15, 2024)
  ----------------------------------------------------------------------------------------------------------------------------------
ins 67 del 38 commentRef 31
comments.xml comments 31
None
[ASSISTANT] Both deliverables are in `output/`:

- **`redlined-arbitration-agreement.docx`**: Cascadian's draft with real tracked changes (67 insertions, 38 deletions) and 31 comments. Each comment gives the playbook section, the tier, what the form says, the markup, and the fallback. Rejecting all changes reproduces the original text paragraph for paragraph; accepting all reads cleanly.
- **`markup-cover-memo.docx`**: addressed to David Ostrander for review first, then Rebecca Stadler. It covers the three client priorities, changes by tier, playbook-tier mismatches, escalation, open decisions, record anomalies, and assumptions.

**What the markup does:** it moves the Agreement to AAA rules, an Atlanta seat, Delaware law, and a three-member panel. It deletes the court-relief waiver and adds a carve-out with emergency arbitration. It also adds fee-shifting, the damages waiver, the class waiver, confidentiality, the expedited track, and optional appellate review. Limitations and document destruction are changed to the playbook positions.

**Decisions needed before this goes out:**
- **Expedited sole arbitrator.** The playbook requires one for capital call, drag-along and buy-sell disputes. Stadler's email calls a sole arbitrator a non-starter. I kept the playbook position and flagged it.
- **Expedited timetable.** Ten business days to appoint, then a hearing up to 30 days later, can leave about one day before the 45-day award deadline. I kept the four numbers and flagged the conflict.
- **Appeal of expedited awards.** A 30-day appeal window stops an expedited award from becoming final. The playbook is silent. The appellate timetable is bracketed for the GC.
- **New York fallback.** Ostrander's email to Stadler mentions a bracketed New York seat. I kept it in the comment only.

**Record problems to check:**
- Hsiao's transmittal is addressed to a domain that is not David's (`hargovewynncalloway.com`). Verify it with her before treating the form as the operative draft.
- The Whitmore recital says the fund is "managed by" Whitmore Capital Partners LLC; the signature block calls it the "General Partner."
- The 48%/24% stakes do not follow the 60%/40% equity split. The totals reconcile.

**Not verified:**
- The Co-Investment Agreement is not in the record. Its governing law, dispute clause, and the notice cross-reference to its Section 11.4 are unchecked.
- The AAA rule titles and the Delaware and New York statute citations come from the playbook. I did not check them.

**Before external circulation:** the comments disclose fallbacks and must be stripped. The file is marked as an internal draft.