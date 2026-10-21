[ASSISTANT] I'll start by inventorying the data room and loading the redline skill that the workspace instructions require.
[ACTION] Bash {"command": "find . -maxdepth 3 -not -path '*/.git*' | head -100 && ls -la output 2>/dev/null; echo; cat LongTermMEMORY.md 2>/dev/null | head -5", "description": "List workspace files and output directory"}
[ACTION] Skill {"skill": "redline-docx"}
[OBSERVATION]
.
./output
./.claude
./.claude/skills
./.claude/skills/redline-docx
./scripts
./scripts/read_doc.py
./documents
./documents/cascadian-counsel-cover-email.eml
./documents/proposed-arbitration-agreement.docx
./documents/whitmore-internal-instructions.eml
./documents/whitmore-arbitration-playbook.docx
./CLAUDE.md
total 0
drwxr-xr-x@ 2 me  staff   64 Oct 19 11:47 .
drwxr-xr-x@ 7 me  staff  224 Oct 19 12:01 ..
[OBSERVATION]
Launching skill: redline-docx
[ACTION] Bash {"command": "python3 scripts/read_doc.py documents/whitmore-arbitration-playbook.docx", "description": "Read the arbitration playbook"}
[ACTION] Bash {"command": "python3 -I -c \"import email,sys;print(email.message_from_binary_file(open(sys.argv[1],'rb')).get_payload(decode=True).decode())\" documents/whitmore-internal-instructions.eml; echo ======; python3 -I -c \"import email,sys;print(email.message_from_binary_file(open(sys.argv[1],'rb')).get_payload(decode=True).decode())\" documents/cascadian-counsel-cover-email.eml", "description": "Decode and read both email files"}
[ACTION] Bash {"command": "python3 scripts/read_doc.py documents/proposed-arbitration-agreement.docx", "description": "Read the proposed arbitration agreement"}
[OBSERVATION]
<persisted-output>
Output too large (44.3KB). Full output saved to: /Users/me/.claude/projects/-Users-me-GoogleHarness2-experiments-lab-sonnet-imp-exec-lab-cc-agg1-arbitration-international-dispute-resolution-draft-markup-of-arbitration-agreement-inv1-work/d7a1e655-1b4d-43a1-8c53-c6e1704e3963/tool-results/bs3jgb5d3.txt

Preview (first 2KB):
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

...
</persisted-output>
[OBSERVATION]
Exit code 1
Priya,

Forwarding the below exchange with Rebecca Stadler, GC at Whitmore Capital Partners, regarding the Vantage Specialty Chemicals / Cascadian Growth Fund co-investment. Pinnacle Winterhaven (Margaret Hsiao) circulated a proposed arbitration agreement — Exhibit F to the Co-Investment Agreement — on January 8. We need a full markup.

Deliverables: (1) redlined markup of the proposed agreement with bracketed comments explaining each change, referencing the playbook, and categorizing every position as Required, Preferred, or Fallback; and (2) a cover memo summarizing all changes by priority tier (critical, important, recommended) with brief legal and commercial rationale.

Source materials: the proposed agreement and the Whitmore Arbitration Playbook (November 2024 version — should be in the deal folder on the DMS). Rebecca's email below highlights her three highest-priority items. The playbook is your baseline for everything else.

Rebecca's three priorities in short: (1) Three-member panel — sole arbitrator is a non-starter at this deal size ($325M equity); standard selection mechanics required. (2) Delete the waiver of court interim relief entirely — non-negotiable — and add emergency arbitrator provisions. (3) Insert expedited procedures for capital call, drag-along, and buy-sell disputes with a 45-day award deadline.

Beyond those three, run the entire agreement against the playbook. I expect significant deviations — the form was drafted by Cascadian's counsel and is tilted their way across the board. Every deviation gets marked up with a comment.

Timeline: I need your draft redline and cover memo by Saturday, January 11, COB so I can review before we send to Rebecca on Sunday. Final goes to Pinnacle Winterhaven by January 13.

Tone guidance: thorough but professional. This is a co-investment relationship, not hostile litigation. Where the playbook identifies a fallback position, note it in the comment so Rebecca can see room for negotiation.

Let me know if you have any questions or if you can't find the playbook in the system — I can send it over. Available by cell if you need to discuss.

David

David Ostrander
Partner
Hargrove, Wynn & Calloway LLP

---

From: David Ostrander <dostrander@hargrovewynn.com>
To: Rebecca Stadler <rstadler@whitmorecapital.com>
Date: Thursday, January 9, 2025, 10:42 AM EST
Subject: RE: Vantage / Cascadian Co-Investment — Arbitration Agreement Review Priorities

Rebecca,

Thanks for the clear direction — we're aligned on all three priority items.

I'm assigning the full markup to Priya Nakamura, a senior associate on the deal team who has worked on several arbitration agreement reviews for Whitmore and knows the playbook well. She'll run the Cascadian form against the November 2024 playbook top to bottom and flag every deviation with comments explaining the playbook basis and categorizing positions as Required, Preferred, or Fallback.

We'll have a draft redline and cover memo to you by end of day Sunday, January 12, for your review before it goes to Pinnacle Winterhaven on the 13th.

The ICC designation and Seattle seat jumped out to me as well — classic counterparty home-cooking. Those will be addressed per the playbook (AAA for domestic transactions, Atlanta as primary seat with New York as a bracketed fallback).

One question: do you want me to call Thomas Riordan or Margaret Hsiao directly to give a heads-up on the scope of the markup, or would you prefer to let the redline speak for itself? Given the number of changes I anticipate, a courtesy call might smooth the path.

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
Subject: Vantage / Cascadian Co-Investment — Arbitration Agreement Review Priorities

David,

I've reviewed the proposed arbitration agreement (Exhibit F to the Co-Investment Agreement) that Margaret Hsiao at Pinnacle Winterhaven circulated yesterday on behalf of Cascadian Growth Fund LP. I have a number of concerns and want to flag my top priorities before your team begins the full markup.

First — the sole arbitrator provision is unacceptable. Whitmore Capital Fund III LP is committing $195 million in equity to the Vantage Specialty Chemicals acquisition, and the total equity check between the two parties is $325 million. Our playbook threshold for a three-member panel is $10 million — we're more than 30x over that threshold. This is a hard no. The markup must require a three-member panel with standard selection mechanics: each side picks one arbitrator, the two party-appointed arbitrators select the chair. Do not present this as a "preferred" position. It is required.

Second — I noticed the proposed agreement includes an express waiver of the right to seek provisional or interim measures from any court of competent jurisdiction. This is non-negotiable. Whitmore must preserve the ability to go to court for injunctive or provisional relief, particularly in scenarios involving breaches of exclusivity, unauthorized transfers, or confidentiality violations. In the Fund II co-investment, we had a situation where we needed emergency TRO relief and it was critical that the arbitration agreement didn't foreclose that option. Delete the waiver entirely and replace it with a carve-out preserving both court-ordered interim relief and emergency arbitrator procedures.

Third — expedited arbitration procedures for capital call disputes, drag-along rights, and buy-sell provisions are critical for fund governance. Capital call disputes cannot sit in a standard arbitration timeline — if a co-investor disputes a capital call, the fund needs resolution within weeks, not months. The playbook requires a 45-day expedited track for these categories of disputes, and I want that reflected in the markup. Cascadian's form has no expedited procedure carve-out at all. Our investment committee has specifically focused on this given the size of the equity commitment and the governance dynamics with a co-investor holding a 24% stake.

Beyond these three items, the full arbitration playbook (last updated November 2024) should govern the markup on all other points. I expect there will be additional issues — the form looks like it was drafted entirely from Cascadian's perspective (Seattle as the seat, ICC as the administering institution, Washington state law). I trust the team to run it against the playbook comprehensively. The markup is due back to Pinnacle Winterhaven by January 13, and I need time to review before it goes out. Please get me a draft by end of day Sunday, January 12.

Let me know if you have questions. Happy to jump on a call if helpful.

Rebecca

Rebecca Stadler
General Counsel
Whitmore Capital Partners LLC
3400 Peachtree Road NE, Suite 1200
Atlanta, GA 30326
(404) 555-0243
rstadler@whitmorecapital.com

(eval):1: ===== not found
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
[ASSISTANT] The proposed agreement is read. The playbook is about 44KB, so I'll read the saved output in sections.
[ACTION] Read {"file_path": "/Users/me/.claude/projects/-Users-me-GoogleHarness2-experiments-lab-sonnet-imp-exec-lab-cc-agg1-arbitration-international-dispute-resolution-draft-markup-of-arbitration-agreement-inv1-work/d7a1e655-1b4d-43a1-8c53-c6e1704e3963/tool-results/bs3jgb5d3.txt", "allow_large": true}
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
[ASSISTANT] I've read the full playbook. Before drafting the spec I need the redline script's spec format and the paragraph indexes.
[ACTION] Bash {"command": "python3 -I .claude/skills/redline-docx/scripts/tracked_redline.py --list documents/proposed-arbitration-agreement.docx 2>&1 | head -150", "description": "List paragraph indexes of the agreement"}
[ACTION] Read {"file_path": "./.claude/skills/redline-docx/scripts/tracked_redline.py", "limit": 120}
[OBSERVATION]
0	EXHIBIT F TO CO-INVESTMENT AGREEMENT
1	ARBITRATION AGREEMENT
2	Dated as of January 15, 2025
3	This Arbitration Agreement (this "Agreement") is entered into as of January 15, 2025, by and between
4	RECITALS
5	WHEREAS, Whitmore Capital Fund III LP, a Delaware limited partnership ("Whitmore"), an investment ve
6	WHEREAS, pursuant to the Co-Investment Agreement, the Parties have agreed to jointly acquire a contr
7	WHEREAS, the Co-Investment Agreement governs, among other things, governance rights, drag-along and 
8	WHEREAS, the Parties desire to establish the terms and procedures by which disputes arising under or
9	NOW, THEREFORE, in consideration of the mutual covenants and agreements set forth in the Co-Investme
10	
11	ARTICLE I — DEFINITIONS
12	As used in this Agreement, the following terms shall have the meanings set forth below:
13	"Agreement" means this Arbitration Agreement, as it may be amended from time to time in accordance w
14	"Arbitral Tribunal" or "Tribunal" means the arbitrator or arbitrators appointed pursuant to Article 
15	"Award" means any interim, partial, or final award rendered by the Arbitral Tribunal in connection w
16	"Claimant" means the Party initiating a Proceeding by filing a request for arbitration.
17	"Co-Investment Agreement" or "CIA" has the meaning set forth in the Recitals.
18	"Company" means Vantage Specialty Chemicals Inc., a Delaware corporation.
19	"Dispute" means any dispute, controversy, or claim arising out of, relating to, or in connection wit
20	"ICC" means the International Chamber of Commerce.
21	"ICC Rules" means the Rules of Arbitration of the International Chamber of Commerce in effect at the
22	"Party" and "Parties" have the meanings set forth in the Recitals.
23	"Proceedings" means any arbitration proceedings commenced pursuant to this Agreement.
24	"Respondent" means the Party against whom a request for arbitration is filed.
25	"Seat" means Seattle, Washington, which shall be the juridical seat of any arbitration conducted und
26	ARTICLE II — AGREEMENT TO ARBITRATE; SCOPE
27	Section 2.1 — Agreement to Arbitrate. Any and all disputes, controversies, or claims arising out of,
28	Section 2.2 — Exclusive Remedy. Arbitration under this Agreement shall be the exclusive remedy for a
29	ARTICLE III — SEAT, LANGUAGE, AND GOVERNING LAW
30	Section 3.1 — Seat of Arbitration. The seat (legal place) of arbitration shall be Seattle, Washingto
31	Section 3.2 — Language. The language of the arbitration shall be English. All submissions, correspon
32	Section 3.3 — Governing Law. This Agreement shall be governed by and construed in accordance with th
33	
34	ARTICLE IV — ARBITRATOR APPOINTMENT AND QUALIFICATIONS
35	Section 4.1 — Number of Arbitrators. The arbitration shall be conducted by a sole arbitrator (the "A
36	Section 4.2 — Appointment Procedure. The Parties shall endeavor to agree upon a mutually acceptable 
37	Section 4.3 — Qualifications. The Arbitrator shall be a neutral individual independent of the Partie
38	ARTICLE V — ARBITRATION PROCEDURES
39	Section 5.1 — Discovery. Discovery shall be conducted in accordance with the ICC Rules, without modi
40	Section 5.2 — Hearings. The Arbitrator shall hold hearings as the Arbitrator deems necessary and app
41	Section 5.3 — Evidence. The Arbitrator shall have the authority to receive and consider such evidenc
42	ARTICLE VI — INTERIM AND EMERGENCY RELIEF
43	Section 6.1 — Waiver of Court Relief. The Parties hereby expressly waive any right to seek provision
44	
45	ARTICLE VII — CONSOLIDATION AND JOINDER
46	Section 7.1 — Consolidation. The Tribunal may, at the request of either Party, consolidate this arbi
47	Section 7.2 — Joinder of Third Parties. Third parties may be joined to the arbitration at the discre
48	ARTICLE VIII — AWARD
49	Section 8.1 — Timing and Form of Award. The Arbitrator shall use best efforts to issue a reasoned aw
50	Section 8.2 — Finality. The award of the Arbitrator shall be final and binding upon the Parties and 
51	Section 8.3 — Remedies. The Arbitrator shall have the authority to award any remedy or relief that a
52	
53	ARTICLE IX — COSTS AND FEES
54	Section 9.1 — Allocation of Costs. Each Party shall bear its own costs and expenses of the arbitrati
55	Section 9.2 — Administrative Costs. The administrative fees and expenses of the ICC and the fees and
56	ARTICLE X — LIMITATIONS PERIOD
57	Section 10.1 — Statute of Limitations. All claims subject to arbitration under this Agreement must b
58	ARTICLE XI — DOCUMENT RETENTION AND DESTRUCTION
59	Section 11.1 — Post-Arbitration Document Handling. The Parties agree that, within thirty (30) days f
60	
61	ARTICLE XII — GENERAL PROVISIONS
62	Section 12.1 — Notices. All notices, requests, demands, and other communications under this Agreemen
63	Section 12.2 — Entire Agreement. This Agreement constitutes the entire agreement between the Parties
64	Section 12.3 — Amendment and Waiver. This Agreement may not be amended, modified, or supplemented ex
65	Section 12.4 — Severability. If any provision of this Agreement is held to be invalid, illegal, or u
66	Section 12.5 — Counterparts. This Agreement may be executed in counterparts, each of which shall be 
67	Section 12.6 — Relationship to Co-Investment Agreement. This Agreement is Exhibit F to and is incorp
68	Section 12.7 — Survival. This Agreement shall survive the termination or expiration of the Co-Invest
69	
70	[Signature Page Follows]
71	
72	IN WITNESS WHEREOF, the Parties have executed this Arbitration Agreement as of the date first writte
73	WHITMORE CAPITAL FUND III LP
74	By: Whitmore Capital Partners LLC, its General Partner
75	By: ________
76	Name: ________
77	Title: ________
78	Date: ________
79	CASCADIAN GROWTH FUND LP
80	By: Cascadian Growth Management LLC, its General Partner
81	By: ________
82	Name: ________
83	Title: ________
84	Date: ________
[OBSERVATION]
1	#!/usr/bin/env python3
2	"""Apply paragraph edits to a .docx as real Word tracked changes (w:ins / w:del).
3	
4	usage: python3 tracked_redline.py <original.docx> <spec.json> <output.docx>
5	
6	spec.json:
7	{
8	  "author": "Firm LLP",                      # optional
9	  "date": "2025-01-11T09:00:00Z",            # optional
10	  "banner": "text for a tracked italic note inserted before the first paragraph",  # optional
11	  "edits":   [{"match": "Section 3.1", "new": "full replacement paragraph text",
12	               "note": "[NOTE -- comment text]"}],     # note optional: tracked italic paragraph after
13	  "inserts": [{"after": "Section 5.3", "text": "**Section 5.4 -- Title.** body", "note": "..."}],
14	  "deletes": [{"match": "Section 6.1", "note": "..."}],   # whole paragraph struck
15	  "notes":   [{"after": "Section 3.2", "note": "[NOTE -- no change]"}]  # comment only
16	}
17	- "match"/"after" = unique start of the paragraph's text (leading text, case-sensitive),
18	  or "#N" for the Nth paragraph (0-based, as listed by --list).
19	- "new"/"text" use **bold** markers for inserted bold; unchanged text keeps its original
20	  formatting. Diff is word-level, so keep unchanged wording identical to the original.
21	- Inserts/notes after the same anchor keep spec order. Fails loudly on a missing or
22	  ambiguous match (lists candidates) -- nothing is written in that case.
23	Operates on the document.xml string, so namespaces/headers/footers are untouched.
24	Also: --list prints "index<TAB>text-start" for every paragraph.
25	"""
26	import difflib, json, re, sys, zipfile
27	from xml.sax.saxutils import escape, unescape
28	
29	P_RE = re.compile(r'<w:p(?: [^>]*)?>.*?</w:p>', re.S)
30	R_RE = re.compile(r'<w:r(?: [^>]*)?>(.*?)</w:r>', re.S)
31	T_RE = re.compile(r'<w:t(?: [^>]*)?>(.*?)</w:t>', re.S)
32	
33	
34	def para_info(px):
35	    ppr = re.search(r'<w:pPr>.*?</w:pPr>', px, re.S)
36	    ppr = ppr.group(0) if ppr else ''
37	    chars = []  # (char, rpr_xml)
38	    for rm in R_RE.finditer(px):
39	        body = rm.group(1)
40	        rpr = re.search(r'<w:rPr>.*?</w:rPr>', body, re.S)
41	        rpr = rpr.group(0) if rpr else ''
42	        for tm in T_RE.finditer(body):
43	            for c in unescape(tm.group(1)):
44	                chars.append((c, rpr))
45	    return ppr, chars
46	
47	
48	def is_bold(rpr): return '<w:b/>' in rpr or '<w:b ' in rpr
49	
50	
51	def strip_fmt(rpr, bold=False, italic=False, color=None):
52	    rpr = re.sub(r'<w:(b|i|u|color)(?: [^>]*)?/>', '', rpr)
53	    add = ('<w:b/>' if bold else '') + ('<w:i/>' if italic else '')
54	    if color: add += '<w:color w:val="%s"/>' % color
55	    if not rpr: return '<w:rPr>%s</w:rPr>' % add if add else ''
56	    return rpr.replace('</w:rPr>', add + '</w:rPr>')
57	
58	
59	class Ctx:
60	    def __init__(self, author, date):
61	        self.author, self.date, self.n = escape(author), date, 1000
62	
63	    def attrs(self):
64	        self.n += 1
65	        return 'w:id="%d" w:author="%s" w:date="%s"' % (self.n, self.author, self.date)
66	
67	
68	def run(rpr, text, deleted=False):
69	    tag = 'w:delText' if deleted else 'w:t'
70	    return '<w:r>%s<%s xml:space="preserve">%s</%s></w:r>' % (rpr, tag, escape(text), tag)
71	
72	
73	def parse_markup(s):
74	    out, bold = [], False
75	    for part in re.split(r'(\*\*)', s):
76	        if part == '**': bold = not bold
77	        else: out.extend((c, bold) for c in part)
78	    return out
79	
80	
81	def group(items, key):
82	    segs = []
83	    for it in items:
84	        k = key(it)
85	        if segs and segs[-1][0] == k: segs[-1][1].append(it)
86	        else: segs.append((k, [it]))
87	    return segs
88	
89	
90	def tokens(chars_text):
91	    return re.findall(r'\s+|\w+|[^\w\s]', chars_text)
92	
93	
94	def edit_paragraph(px, new_markup, ctx):
95	    ppr, ochars = para_info(px)
96	    new = parse_markup(new_markup)
97	    otext, ntext = ''.join(c for c, _ in ochars), ''.join(c for c, _ in new)
98	    ot, nt = tokens(otext), tokens(ntext)
99	    base = next((r for c, r in ochars if not is_bold(r)), ochars[0][1] if ochars else '')
100	    base = strip_fmt(base)
101	    out, oi, ni = [], 0, 0
102	    sm = difflib.SequenceMatcher(None, ot, nt, autojunk=False)
103	
104	    def emit_orig(a, b, deleted):
105	        for rpr, grp in group(ochars[a:b], lambda x: x[1]):
106	            txt = ''.join(c for c, _ in grp)
107	            out.append('<w:del %s>%s</w:del>' % (ctx.attrs(), run(rpr, txt, True)) if deleted else run(rpr, txt))
108	
109	    def emit_new(a, b):
110	        for bold, grp in group(new[a:b], lambda x: x[1]):
111	            txt = ''.join(c for c, _ in grp)
112	            rpr = strip_fmt(base, bold=bold)
113	            out.append('<w:ins %s>%s</w:ins>' % (ctx.attrs(), run(rpr, txt)))
114	
115	    opos = [0]; [opos.append(opos[-1] + len(t)) for t in ot]
116	    npos = [0]; [npos.append(npos[-1] + len(t)) for t in nt]
117	    for tag, i1, i2, j1, j2 in sm.get_opcodes():
118	        if tag == 'equal': emit_orig(opos[i1], opos[i2], False)
119	        else:
120	            if i2 > i1: emit_orig(opos[i1], opos[i2], True)
[ASSISTANT] The paragraph list gives me the anchors I need. I have the full playbook and the draft, so I'll set the position for each clause before writing the spec.

Key calls I'm making:
- **Source hierarchy:** Rebecca's email governs the three priorities: the panel selection mechanics are treated as Required, the 45-day expedited track is Critical, and the court-relief waiver is deleted.
- **Two classification axes:** Required/Preferred/Fallback and Critical/Important/Recommended, kept separate.
- **Conflicts to flag:** the expedited 30-day hearing window does not fit a 45-day award; discovery is Required in §8 but Recommended in §22; the class waiver's "consolidated" wording collides with the consent-based consolidation clause; the Co-Investment Agreement is not in the data room.

I'll write the spec in a scratch directory outside `documents/` and `output/`.
[ACTION] Bash {"command": "mkdir -p /tmp/redline-scratch && cd . && grep -n \"date\\|author\" .claude/skills/redline-docx/scripts/tracked_redline.py | sed -n '1,40p'", "description": "Create scratch dir and check author/date handling in script"}
[OBSERVATION]
8:  "author": "Firm LLP",                      # optional
9:  "date": "2025-01-11T09:00:00Z",            # optional
22:  ambiguous match (lists candidates) -- nothing is written in that case.
60:    def __init__(self, author, date):
61:        self.author, self.date, self.n = escape(author), date, 1000
65:        return 'w:id="%d" w:author="%s" w:date="%s"' % (self.n, self.author, self.date)
158:    ctx = Ctx(spec.get('author', 'Reviewer'), spec.get('date', '2025-01-01T00:00:00Z'))
[ACTION] Write {"file_path": "/tmp/redline-scratch/spec.json", "content": "{\n  \"author\": \"Hargrove, Wynn & Calloway LLP\",\n  \"banner\": \"[PRIVILEGED & CONFIDENTIAL -- Whitmore internal review draft. Bracketed notes cite the Whitmore Arbitration Playbook v3.0 (Nov. 15, 2024) and fallback positions. Delete all notes before any circulation to Cascadian or Pinnacle Winterhaven.]\",\n  \"edits\": [\n    {\"match\": \"\\\"ICC\\\" means\",\n     \"new\": \"\\\"AAA\\\" means the American Arbitration Association.\",\n     \"note\": \"[NOTE -- Classification: Required (Playbook s.2). Tier: Important. ICC is reserved for cross-border deals and may never administer a purely domestic U.S. transaction. All parties, the Target (Houston, TX) and the equity are U.S.-based. Fallback: JAMS Comprehensive Rules if Cascadian objects to AAA.]\"},\n    {\"match\": \"\\\"ICC Rules\\\" means\",\n     \"new\": \"\\\"AAA Rules\\\" means the Commercial Arbitration Rules of the AAA in effect at the time of commencement of the arbitration.\",\n     \"note\": \"[NOTE -- Classification: Preferred (Playbook s.2): AAA Commercial Rules, most current version as of submission. Conforming change.]\"},\n    {\"match\": \"\\\"Seat\\\" means\",\n     \"new\": \"\\\"Seat\\\" means Atlanta, Georgia, which shall be the juridical seat of any arbitration conducted under this Agreement.\",\n     \"note\": \"[NOTE -- Conforming change to Section 3.1.]\"},\n    {\"match\": \"Section 2.1\",\n     \"new\": \"Section 2.1 \u2014 Agreeme
[OBSERVATION]
File created successfully at: /tmp/redline-scratch/spec.json (file state is current in your context — no need to Read it back)
[ASSISTANT] I left a placeholder insert in the spec by mistake, and the `ARTICLE XI` match would be ambiguous with `ARTICLE XII`. Fixing both before the build.
[ACTION] Edit {"replace_all": false, "file_path": "/tmp/redline-scratch/spec.json", "old_string": "    {\"after\": \"Section 10.1\",\n     \"text\": \"\",\n     \"note\": \"[NOTE -- Placeholder removed in final draft; no text inserted.]\"}\n  ],", "new_string": "  ],"}
[ACTION] Edit {"replace_all": false, "file_path": "/tmp/redline-scratch/spec.json", "old_string": "    {\"match\": \"ARTICLE XI\",\n     \"new\": \"ARTICLE XI \u2014 DOCUMENT RETENTION\"},", "new_string": "    {\"match\": \"ARTICLE XI \u2014\",\n     \"new\": \"ARTICLE XI \u2014 DOCUMENT RETENTION\"},"}
[OBSERVATION]
The file /tmp/redline-scratch/spec.json has been updated successfully. (file state is current in your context — no need to Read it back)
[OBSERVATION]
The file /tmp/redline-scratch/spec.json has been updated successfully. (file state is current in your context — no need to Read it back)
[ACTION] Bash {"command": "python3 -I .claude/skills/redline-docx/scripts/tracked_redline.py documents/proposed-arbitration-agreement.docx /tmp/redline-scratch/spec.json output/redlined-arbitration-agreement.docx; echo \"exit=$?\"", "description": "Build tracked-changes redline from the spec"}
[OBSERVATION]
Traceback (most recent call last):
  File "./.claude/skills/redline-docx/scripts/tracked_redline.py", line 209, in <module>
    main()
    ~~~~^^
  File "./.claude/skills/redline-docx/scripts/tracked_redline.py", line 155, in main
    spec = json.load(open(specf, encoding='utf-8'))
  File "/Library/Frameworks/Python.framework/Versions/3.15/lib/python3.15/json/__init__.py", line 306, in load
    return loads(fp.read(),
        cls=cls, object_hook=object_hook,
        parse_float=parse_float, parse_int=parse_int,
        parse_constant=parse_constant, object_pairs_hook=object_pairs_hook,
        array_hook=array_hook, **kw)
  File "/Library/Frameworks/Python.framework/Versions/3.15/lib/python3.15/json/__init__.py", line 371, in loads
    return _default_decoder.decode(s)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "/Library/Frameworks/Python.framework/Versions/3.15/lib/python3.15/json/decoder.py", line 358, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.15/lib/python3.15/json/decoder.py", line 374, in raw_decode
    obj, end = self.scan_once(s, idx)
               ~~~~~~~~~~~~~~^^^^^^^^
json.decoder.JSONDecodeError: Illegal trailing comma before end of array: line 100 column 322 (char 22921)
exit=1
[ACTION] Edit {"replace_all": false, "file_path": "/tmp/redline-scratch/spec.json", "old_string": "Escalate to GC before accepting a narrower waiver.]\"},\n  ],", "new_string": "Escalate to GC before accepting a narrower waiver.]\"}\n  ],"}
[OBSERVATION]
The file /tmp/redline-scratch/spec.json has been updated successfully. (file state is current in your context — no need to Read it back)
[ACTION] Bash {"command": "python3 -I -c \"import json,sys; json.load(open(sys.argv[1],encoding='utf-8')); print('json ok')\" /tmp/redline-scratch/spec.json && python3 -I .claude/skills/redline-docx/scripts/tracked_redline.py documents/proposed-arbitration-agreement.docx /tmp/redline-scratch/spec.json output/redlined-arbitration-agreement.docx; echo \"exit=$?\"", "description": "Validate spec JSON and rebuild the redline"}
[OBSERVATION]
json ok
Traceback (most recent call last):
  File "./.claude/skills/redline-docx/scripts/tracked_redline.py", line 209, in <module>
    main()
    ~~~~^^
  File "./.claude/skills/redline-docx/scripts/tracked_redline.py", line 180, in main
    repl[i] = edit_paragraph(paras[i], e['new'], ctx); add_note(i, e.get('note'))
                                       ~^^^^^^^
KeyError: 'new'
exit=1
[ASSISTANT] The Section 6.1 deletion is in the `edits` array instead of `deletes`. I'll move it with a small JSON rewrite of my own scratch spec.
[ACTION] Bash {"command": "cd /tmp/redline-scratch && python3 -I -c \"\nimport json\np='/tmp/redline-scratch/spec.json'\ns=json.load(open(p,encoding='utf-8'))\nd=[e for e in s['edits'] if e.get('delete')]\ns['edits']=[e for e in s['edits'] if not e.get('delete')]\nfor e in d: e.pop('delete')\ns['deletes']=d\njson.dump(s,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)\nprint('edits',len(s['edits']),'deletes',len(s['deletes']),'inserts',len(s['inserts']),'notes',len(s['notes']))\n\" && cd . && python3 -I .claude/skills/redline-docx/scripts/tracked_redline.py documents/proposed-arbitration-agreement.docx /tmp/redline-scratch/spec.json output/redlined-arbitration-agreement.docx; echo \"exit=$?\"", "description": "Move the 6.1 deletion into the deletes list and rebuild"}
[OBSERVATION]
edits 24 deletes 1 inserts 7 notes 1
wrote output/redlined-arbitration-agreement.docx: 24 edits, 1 deletes, 7 inserts, 38 notes, 412 revision marks
exit=0
[ASSISTANT] The build succeeded: 24 edits, 1 deletion, 7 inserts, 38 notes. Next I'll run the checker, grepping for the superseded terms and writing the accepted view for reading.
[ACTION] Bash {"command": "python3 -I .claude/skills/redline-docx/scripts/check_redline.py documents/proposed-arbitration-agreement.docx output/redlined-arbitration-agreement.docx --grep \"International Chamber\" \"ICC\" \"Seattle\" \"Washington\" \"sole arbitrator\" \"destruction\" \"destroy\" \"one (1) year\" \"waive\" \"best efforts\" \"without modification\" --accepted /tmp/redline-scratch/accepted.txt; echo \"exit=$?\"", "description": "Run redline checker with superseded-term greps"}
[OBSERVATION]
revisions: 253 insertions, 159 deletions
OK: reject-all text == original (78 paragraphs)
accepted view contains 'International Chamber' in 0 paragraph(s)
accepted view contains 'ICC' in 3 paragraph(s)
   - [NOTE -- Classification: Required (Playbook s.2). Tier: Important. ICC is reserved for cross-border deals and may never administer a purely 
   - [NOTE -- Mechanics classified Preferred in Playbook s.4(a)-(c), but treated as Required per R. Stadler's instruction (1/9/25): "standard sel
   - [NOTE -- Conforming change to Section 9.1; ICC reference replaced with AAA.]
accepted view contains 'Seattle' in 2 paragraph(s)
   - WHEREAS, Whitmore Capital Fund III LP, a Delaware limited partnership ("Whitmore"), an investment vehicle managed by Whitmore Capital Partne
   - [NOTE -- Classification: Required (Playbook s.3). Tier: Important. Seattle is Cascadian's home jurisdiction and is categorically NOT ACCEPTA
accepted view contains 'Washington' in 1 paragraph(s)
   - [NOTE -- Classification: Required (Playbook s.6). Tier: Critical. Washington is Cascadian's home-state law and is categorically NOT ACCEPTAB
accepted view contains 'sole arbitrator' in 2 paragraph(s)
   - Section 4.3 — Qualifications. Each Arbitrator, including any sole arbitrator appointed under Section 5.4, shall (a) have at least fifteen (1
   - Section 5.4 — Expedited Procedures for Capital Call, Drag-Along, and Buy-Sell Disputes. Notwithstanding Sections 4.1, 4.2, 5.1, and 8.1, any
accepted view contains 'destruction' in 1 paragraph(s)
   - [NOTE -- Classification: Required; destruction clauses are NOT ACCEPTABLE at any time period (Playbook s.20). Tier: Important. The destructi
accepted view contains 'destroy' in 1 paragraph(s)
   - Section 11.1 — Document Retention. The Parties shall not destroy, and shall retain for a minimum of seven (7) years following the issuance o
accepted view contains 'one (1) year' in 0 paragraph(s)
accepted view contains 'waive' in 8 paragraph(s)
   - [NOTE -- Classification: Required; waiver of court interim relief is NOT ACCEPTABLE (Playbook s.10). Tier: Critical. Deleted in full, with t
   - Section 6.2 — Court Interim Relief Preserved. Notwithstanding Sections 2.1 and 2.2, any Party may at any time before, during, or after the a
   - [NOTE -- Classification: Required (Playbook s.10), with the Preferred anti-waiver statement included. Tier: Critical. Preserves court relief
   - Section 8.2 — Finality. Subject to Section 8.4, the Award of the Arbitral Tribunal shall be final and binding upon the Parties and shall not
   - [NOTE -- Conforming change. The deleted sentence (no limit on types or amounts of damages) conflicts with the damages waiver in Section 8.5 
   - Section 8.5 — Damages Limitations. To the fullest extent permitted by law, each Party waives any right to recover from the other Party punit
   - [NOTE -- Classification: Required (Playbook s.13), with the fraud/willful misconduct carve-out required. Tier: Important. Mutual, applies re
   - Section 12.3 — Amendment and Waiver. This Agreement may not be amended, modified, or supplemented except by a written instrument signed by b
accepted view contains 'best efforts' in 0 paragraph(s)
accepted view contains 'without modification' in 0 paragraph(s)
accepted view -> /tmp/redline-scratch/accepted.txt
exit=0
[ASSISTANT] The reject-all check passes: rejecting every change restores the original text. The remaining hits are intended: notes that cite the superseded terms, Cascadian's Seattle address in the recitals, and the expedited sole arbitrator. Next I'll read the accepted view end to end.
[ACTION] Read {"file_path": "/tmp/redline-scratch/accepted.txt"}
[OBSERVATION]
1	[PRIVILEGED & CONFIDENTIAL -- Whitmore internal review draft. Bracketed notes cite the Whitmore Arbitration Playbook v3.0 (Nov. 15, 2024) and fallback positions. Delete all notes before any circulation to Cascadian or Pinnacle Winterhaven.]
2	EXHIBIT F TO CO-INVESTMENT AGREEMENT
3	ARBITRATION AGREEMENT
4	Dated as of January 15, 2025
5	This Arbitration Agreement (this "Agreement") is entered into as of January 15, 2025, by and between the following parties in connection with that certain Co-Investment Agreement dated as of even date herewith (the "Co-Investment Agreement"). Capitalized terms used but not otherwise defined herein shall have the meanings ascribed to them in the Co-Investment Agreement.
6	RECITALS
7	WHEREAS, Whitmore Capital Fund III LP, a Delaware limited partnership ("Whitmore"), an investment vehicle managed by Whitmore Capital Partners LLC, a Delaware limited liability company, with its principal office at 3400 Peachtree Road NE, Suite 1200, Atlanta, GA 30326, and Cascadian Growth Fund LP, a Delaware limited partnership ("Cascadian"), managed by its general partner, Cascadian Growth Management LLC, a Delaware limited liability company, with its principal office at 1501 Fourth Avenue, Suite 3700, Seattle, WA 98101 (each, a "Party" and together, the "Parties"), have entered into that certain Co-Investment Agreement dated as of January 15, 2025 (the "Co-Investment Agreement");
8	WHEREAS, pursuant to the Co-Investment Agreement, the Parties have agreed to jointly acquire a controlling interest (approximately 72%) of Vantage Specialty Chemicals Inc., a Delaware corporation headquartered at 10200 Bellaire Boulevard, Suite 400, Houston, TX 77072 (the "Target" or the "Company"), at a total enterprise value of $680,000,000, with Whitmore contributing $195,000,000 in equity for a 48% equity stake and Cascadian contributing $130,000,000 in equity for a 24% equity stake, for total equity of $325,000,000, with the remaining $355,000,000 in debt financing;
9	WHEREAS, the Co-Investment Agreement governs, among other things, governance rights, drag-along and tag-along rights, transfer restrictions, and capital call mechanics relating to the Parties' investment in the Company; and
10	WHEREAS, the Parties desire to establish the terms and procedures by which disputes arising under or in connection with the Co-Investment Agreement shall be resolved.
11	NOW, THEREFORE, in consideration of the mutual covenants and agreements set forth in the Co-Investment Agreement, and for other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the Parties agree as follows:
12	
13	ARTICLE I — DEFINITIONS
14	As used in this Agreement, the following terms shall have the meanings set forth below:
15	"Agreement" means this Arbitration Agreement, as it may be amended from time to time in accordance with its terms.
16	"Arbitral Tribunal" or "Tribunal" means the arbitrator or arbitrators appointed pursuant to Article IV of this Agreement to resolve a Dispute.
17	"Award" means any interim, partial, or final award rendered by the Arbitral Tribunal in connection with any Proceedings.
18	"Claimant" means the Party initiating a Proceeding by filing a request for arbitration.
19	"Co-Investment Agreement" or "CIA" has the meaning set forth in the Recitals.
20	"Company" means Vantage Specialty Chemicals Inc., a Delaware corporation.
21	"Dispute" means any dispute, controversy, or claim arising out of, relating to, or in connection with this Agreement or the Co-Investment Agreement, including any question regarding the existence, formation, validity, interpretation, performance, breach, or termination thereof.
22	"AAA" means the American Arbitration Association.
23	[NOTE -- Classification: Required (Playbook s.2). Tier: Important. ICC is reserved for cross-border deals and may never administer a purely domestic U.S. transaction. All parties, the Target (Houston, TX) and the equity are U.S.-based. Fallback: JAMS Comprehensive Rules if Cascadian objects to AAA.]
24	"AAA Rules" means the Commercial Arbitration Rules of the AAA in effect at the time of commencement of the arbitration.
25	[NOTE -- Classification: Preferred (Playbook s.2): AAA Commercial Rules, most current version as of submission. Conforming change.]
26	"Party" and "Parties" have the meanings set forth in the Recitals.
27	"Proceedings" means any arbitration proceedings commenced pursuant to this Agreement.
28	"Respondent" means the Party against whom a request for arbitration is filed.
29	"Seat" means Atlanta, Georgia, which shall be the juridical seat of any arbitration conducted under this Agreement.
30	[NOTE -- Conforming change to Section 3.1.]
31	ARTICLE II — AGREEMENT TO ARBITRATE; SCOPE
32	Section 2.1 — Agreement to Arbitrate. Any and all disputes, controversies, or claims arising out of, relating to, or in connection with this Agreement or the Co-Investment Agreement, including but not limited to the formation, validity, interpretation, performance, breach, or termination thereof (each, a "Dispute"), shall be exclusively and finally resolved by binding arbitration administered by the American Arbitration Association in accordance with the AAA Rules in effect at the time of the filing of the request for arbitration. The Parties acknowledge and agree that this Agreement evidences a transaction involving commerce and that the Federal Arbitration Act, 9 U.S.C. §§ 1--16, shall govern the interpretation and enforcement of this Agreement.
33	[NOTE -- Conforming change to Playbook s.2 (Required: AAA). Scope language is unchanged and already meets s.7 (Required: broad scope).]
34	Section 2.2 — Exclusive Remedy. Arbitration under this Agreement shall be the exclusive remedy for any Dispute, and no Party shall institute any action or proceeding in any court with respect to any Dispute, except (a) as provided in Article VI and (b) in any proceeding to confirm, enforce, or vacate an Award.
35	[NOTE -- Classification: Required (Playbook s.10). Tier: Critical. Express carve-out from the agreement to arbitrate for interim relief (Article VI), plus award enforcement and vacatur (Playbook s.9(ii)).]
36	Section 2.3 — Individual Basis. The Parties agree that any arbitration under this Agreement shall be conducted on an individual basis only. No Party may bring or participate in any class, collective, consolidated, or representative proceeding in arbitration or in any court. The Arbitral Tribunal shall have no authority to preside over any form of class, collective, or representative proceeding.
37	[NOTE -- Classification: Required, with no fallback (Playbook s.16). Tier: Critical. Required language used substantially verbatim. Absent from the draft. Tension: "consolidated" in this clause bars consolidated proceedings outright, while Section 7.1 permits consolidation with unanimous consent. Confirm whether the bar should cover class-type consolidation only.]
38	ARTICLE III — SEAT, LANGUAGE, AND GOVERNING LAW
39	Section 3.1 — Seat of Arbitration. The seat (legal place) of arbitration shall be Atlanta, Georgia. Any hearings shall be conducted at the Seat unless otherwise agreed by the Parties or ordered by the Arbitral Tribunal.
40	[NOTE -- Classification: Required (Playbook s.3). Tier: Important. Seattle is Cascadian's home jurisdiction and is categorically NOT ACCEPTABLE. Atlanta is Whitmore's home seat. Fallback: New York, New York if Cascadian objects to Atlanta.]
41	Section 3.2 — Language. The language of the arbitration shall be English. All submissions, correspondence, evidence, and hearings shall be conducted in English.
42	Section 3.3 — Governing Law. This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to its conflict of laws principles.
43	[NOTE -- Classification: Required (Playbook s.6). Tier: Critical. Washington is Cascadian's home-state law and is categorically NOT ACCEPTABLE. Fallback: New York law. The Co-Investment Agreement must also be Delaware-governed (s.6). The CIA is not in the data room and has not been reviewed.]
44	
45	ARTICLE IV — ARBITRATOR APPOINTMENT AND QUALIFICATIONS
46	Section 4.1 — Number of Arbitrators. Except as provided in Section 5.4, the arbitration shall be conducted by three (3) arbitrators (each, an "Arbitrator") constituting the Arbitral Tribunal, appointed in accordance with Section 4.2 and the AAA Rules.
47	[NOTE -- Classification: Required (three-member tribunal for disputes over $10M; Playbook s.4). Tier: Critical. Per R. Stadler (1/9/25), this is a hard requirement for a $325M equity transaction. The sole-arbitrator fallback (disputes of $10M or less) is not offered.]
48	Section 4.2 — Appointment Procedure. Each Party shall appoint one Arbitrator within thirty (30) days following the filing of the request for arbitration. The two party-appointed Arbitrators shall jointly select the presiding Arbitrator (chair) within twenty (20) days following the appointment of the second party-appointed Arbitrator. If the two party-appointed Arbitrators do not agree on the chair within such twenty (20)-day period, the AAA shall appoint the chair from its roster of qualified arbitrators in accordance with the AAA Rules.
49	[NOTE -- Mechanics classified Preferred in Playbook s.4(a)-(c), but treated as Required per R. Stadler's instruction (1/9/25): "standard selection mechanics required." Tier: Critical. Replaces ICC appointment.]
50	Section 4.3 — Qualifications. Each Arbitrator, including any sole arbitrator appointed under Section 5.4, shall (a) have at least fifteen (15) years of professional experience in private equity, mergers and acquisitions, or corporate finance, including as an attorney, investment banker, or financial advisor in those fields, or as an arbitrator in disputes involving those fields; (b) be a member of the AAA's National Roster of Arbitrators; and (c) be a neutral individual independent of the Parties, and not have had any professional, financial, or personal relationship with any Party, any affiliate of a Party, or any counsel of record within the five (5) years preceding appointment.
51	[NOTE -- Classification: Required (Playbook s.5). Tier: Recommended. Fallback: 10 years of experience, only with prior GC approval. Not offered in this markup.]
52	ARTICLE V — ARBITRATION PROCEDURES
53	Section 5.1 — Discovery. Discovery shall be conducted in accordance with the AAA Rules, as modified by this Section 5.1. Each Party may take up to three (3) fact depositions, each not to exceed seven (7) hours of testimony on the record; may serve up to fifteen (15) document requests (including subparts); and may retain one (1) testifying expert. Expert reports shall be exchanged simultaneously on a date set by the Arbitral Tribunal. The Arbitral Tribunal shall have the authority to manage discovery within these limits as it deems appropriate in the interests of efficiency and proportionality.
54	[NOTE -- Classification: Required (Playbook s.8 body). Tier: Recommended in the s.22 summary but Required in the s.8 body. Treated as Required; confirm with GC. Fallback: "limited and proportional" language, with the 3-deposition and 1-expert caps as non-negotiable minimums.]
55	Section 5.2 — Hearings. The Arbitral Tribunal shall hold hearings as it deems necessary and appropriate. Hearings shall be held at the Seat unless otherwise agreed by the Parties or directed by the Arbitral Tribunal.
56	[NOTE -- Conforming change to Sections 5.2 and 5.3 ("Arbitrator" replaced with "Arbitral Tribunal" for the three-member panel).]
57	Section 5.3 — Evidence. The Arbitral Tribunal shall have the authority to receive and consider such evidence as it deems relevant and material, including documentary evidence, witness testimony, and expert reports. The Arbitral Tribunal shall determine the admissibility, relevance, materiality, and weight of any evidence offered.
58	Section 5.4 — Expedited Procedures for Capital Call, Drag-Along, and Buy-Sell Disputes. Notwithstanding Sections 4.1, 4.2, 5.1, and 8.1, any Dispute concerning (a) the timing, amount, validity, or enforceability of a capital call; (b) the exercise, conditions, pricing, or procedural requirements of a drag-along right; or (c) the triggering, valuation, mechanics, or timing of a buy-sell (shotgun) provision (each, an "Expedited Dispute") shall be resolved as follows: (i) the Arbitral Tribunal shall consist of a sole arbitrator meeting the requirements of Section 4.3, agreed by the Parties or, failing agreement, appointed by the AAA, in each case within ten (10) business days after the filing of the request for arbitration; (ii) the hearing shall be conducted within thirty (30) days after the appointment of the sole arbitrator; (iii) discovery shall be limited to document production, with no depositions and no more than five (5) document requests per Party; and (iv) the Arbitral Tribunal shall render its final Award within forty-five (45) days after the filing of the request for arbitration.
59	[NOTE -- Classification: Required (Playbook s.17). Tier: Critical per R. Stadler (1/9/25); the s.22 summary lists this as Recommended. Fallback: award deadline up to 60 days, but no longer. INTERNAL TENSION: the 30-day hearing window cannot be reconciled with a 45-day award. Appointment at day 14 (10 business days) puts the hearing at day 44, leaving about one day for a reasoned award that includes findings of fact and conclusions of law. Before sending, either shorten the hearing window (e.g., to about 21 days after appointment) or accept the 60-day fallback. See cover memo.]
60	Section 5.5 — Confidentiality. The Parties shall keep strictly confidential (a) the existence of any Proceedings; (b) all submissions, briefs, motions, and pleadings filed in the Proceedings; (c) all evidence, testimony, exhibits, and documents produced or presented in the Proceedings; (d) all orders, rulings, and Awards issued by the Arbitral Tribunal; and (e) all communications between the Parties and the Arbitral Tribunal. This obligation does not apply to disclosures (i) required by applicable law, regulation, or order of a court of competent jurisdiction, including SEC reporting obligations, tax reporting, and regulatory inquiries; (ii) necessary for the enforcement, confirmation, or vacatur of an Award in a court of competent jurisdiction; or (iii) to attorneys, accountants, and financial advisors subject to professional duties of confidentiality, provided such advisors agree to be bound by this Section 5.5. A breach or threatened breach of this Section 5.5 may cause irreparable harm, and the non-breaching Party may seek injunctive relief, including emergency relief, in accordance with Article VI.
61	[NOTE -- Classification: Required (Playbook s.9). Tier: Important. Absent from the draft; the playbook does not permit its absence. Exceptions are limited to those in s.9. Injunctive relief for breach is included (Preferred). Liquidated damages are not included.]
62	ARTICLE VI — INTERIM AND EMERGENCY RELIEF
63	[NOTE -- Classification: Required; waiver of court interim relief is NOT ACCEPTABLE (Playbook s.10). Tier: Critical. Deleted in full, with the carve-out in Section 6.2 substituted. R. Stadler (1/9/25) identifies this as non-negotiable. Any counter-proposal restricting court relief goes to the GC immediately.]
64	Section 6.2 — Court Interim Relief Preserved. Notwithstanding Sections 2.1 and 2.2, any Party may at any time before, during, or after the arbitration seek provisional, interim, conservatory, or injunctive measures, including temporary restraining orders, preliminary injunctions, attachments, and asset-freezing orders, from any court of competent jurisdiction. Seeking such relief shall not constitute a waiver of the right to arbitrate, is not inconsistent with this Agreement, and shall not be deemed a submission to the jurisdiction of such court for any purpose other than the relief sought.
65	[NOTE -- Classification: Required (Playbook s.10), with the Preferred anti-waiver statement included. Tier: Critical. Preserves court relief for the scenarios R. Stadler identified: breach of exclusivity, unauthorized transfers, and confidentiality violations.]
66	Section 6.3 — Emergency Arbitrator. Before the Arbitral Tribunal is constituted, any Party may apply for emergency measures of protection under the AAA Optional Rules for Emergency Measures of Protection in effect at the time of the application. An emergency arbitrator order does not substitute for relief from a court under Section 6.2, and a Party may seek relief from a court under Section 6.2 whether or not an emergency arbitrator application has been made.
67	[NOTE -- Classification: Required (Playbook s.10): incorporate the administering institution's emergency arbitrator provisions. Tier: Critical. Supplements court relief and does not replace it.]
68	
69	ARTICLE VII — CONSOLIDATION AND JOINDER
70	Section 7.1 — Consolidation. No arbitration under this Agreement shall be consolidated with any other arbitration, whether arising out of or in connection with the Co-Investment Agreement, any other agreement between the Parties, or involving a party to this Agreement, except with the prior written consent of all Parties to all proceedings proposed to be consolidated. The Arbitral Tribunal shall have no authority to order consolidation absent such consent, and no Party may compel consolidation over the objection of another Party.
71	[NOTE -- Classification: Required (Playbook s.11). Tier: Important. The tribunal's discretionary consolidation power is removed. Fallback: consent of all claimants and respondents across all proceedings, plus approval by the tribunal(s).]
72	Section 7.2 — Joinder of Third Parties. No third party may be joined to any arbitration under this Agreement except with the prior written consent of all existing Parties to the arbitration and the written consent of the third party to be joined. Any joined third party shall agree in writing to be bound by this Agreement and by all procedural orders previously issued by the Arbitral Tribunal.
73	[NOTE -- Classification: Required (Playbook s.12). Tier: Important. Joinder at the tribunal's discretion is NOT ACCEPTABLE. No fallback: unanimous consent is non-negotiable.]
74	ARTICLE VIII — AWARD
75	Section 8.1 — Timing and Form of Award. Except as provided in Section 5.4, the Arbitral Tribunal shall render its final Award within ninety (90) days of the close of Proceedings, which shall be the date on which the last post-hearing submission is filed or the hearing transcript is received by the Arbitral Tribunal, whichever is later. The Award shall be in writing and shall set forth detailed findings of fact and conclusions of law. Failure to render the Award within such period shall not affect the validity of the Award or the jurisdiction of the Arbitral Tribunal.
76	[NOTE -- Classification: Required (Playbook s.18: 90 days; findings of fact and conclusions of law). Tier: Recommended. The draft's 120-day period is the playbook fallback and is not offered. Fallback: up to 120 days, but findings of fact and conclusions of law are non-negotiable.]
77	Section 8.2 — Finality. Subject to Section 8.4, the Award of the Arbitral Tribunal shall be final and binding upon the Parties and shall not be subject to appeal, except as otherwise provided by applicable law. Judgment upon the Award may be entered in any court of competent jurisdiction. The Parties hereby waive, to the fullest extent permitted by law, any right to appeal or challenge the Award, except on the limited grounds set forth in the Federal Arbitration Act or as provided in Section 8.4.
78	[NOTE -- Conforming change to Section 8.4 (appellate arbitration).]
79	Section 8.3 — Remedies. The Arbitral Tribunal shall have the authority to award any remedy or relief that a court of competent jurisdiction could grant, including but not limited to specific performance, injunctive relief, and monetary damages, subject to Section 8.5.
80	[NOTE -- Conforming change. The deleted sentence (no limit on types or amounts of damages) conflicts with the damages waiver in Section 8.5 (Playbook s.13).]
81	Section 8.4 — Optional Appellate Arbitration. For any Award (or series of Awards in a single Proceeding) that exceeds $25,000,000 in aggregate monetary relief, including damages, interest, fees, and costs, either Party may elect to appeal under the AAA Optional Appellate Arbitration Rules by filing a notice of appeal within thirty (30) days after issuance of the Award. The appellate panel shall consist of three (3) arbitrators drawn from the AAA's appellate roster, and the standard of review shall be as set forth in such rules. The Award shall not become final and enforceable until the appeal period has expired without a notice of appeal having been filed, or until the appellate panel has issued its decision.
82	[NOTE -- Classification: Required for awards over $25M (Playbook s.19). Tier: Important. This transaction ($325M equity) is above the threshold. Fallback: appellate arbitration by post-award mutual written consent, if Cascadian objects to mandatory appeal.]
83	Section 8.5 — Damages Limitations. To the fullest extent permitted by law, each Party waives any right to recover from the other Party punitive, exemplary, or consequential damages, including lost profits, lost opportunities, diminution in value of other investments, and reputational harm, arising out of or relating to any Dispute, whether under contract, tort, equity, or otherwise. This waiver shall not apply in cases of fraud or willful misconduct, in which case the Arbitral Tribunal may award any damages available under applicable law.
84	[NOTE -- Classification: Required (Playbook s.13), with the fraud/willful misconduct carve-out required. Tier: Important. Mutual, applies regardless of legal theory (Preferred). Fallback: punitive and exemplary waiver only, with the carve-out preserved. Escalate to GC before accepting a narrower waiver.]
85	
86	ARTICLE IX — COSTS AND FEES
87	Section 9.1 — Allocation of Costs. The substantially prevailing Party shall be entitled to recover from the non-prevailing Party its reasonable attorneys' fees, expert witness fees, arbitrator fees, administrative fees, and other costs of the arbitration, as determined by the Arbitral Tribunal in the Award.
88	[NOTE -- Classification: Required (Playbook s.14). Tier: Important. Draft's "each Party bears its own costs regardless of outcome" is NOT ACCEPTABLE. Preferred: tribunal determines the substantially prevailing party and reasonableness. Fallback: tribunal discretion to allocate by relative success (GC escalation before accepting).]
89	Section 9.2 — Administrative Costs. The administrative fees and expenses of the AAA and the fees and expenses of the Arbitral Tribunal shall be advanced equally by the Parties, subject to reallocation in the Award in accordance with Section 9.1.
90	[NOTE -- Conforming change to Section 9.1; ICC reference replaced with AAA.]
91	ARTICLE X — LIMITATIONS PERIOD
92	Section 10.1 — Statute of Limitations. Nothing in this Agreement shortens or otherwise modifies the statute of limitations applicable to any claim subject to arbitration under this Agreement, which shall be the period provided under the governing law set forth in Section 3.3.
93	[NOTE -- Classification: Required (Playbook s.15). Tier: Critical. The one-year limitations period is NOT ACCEPTABLE. It is shorter than the 3-year Delaware statutory period (10 Del. C. s.8106) and could expire before quarterly and annual reporting reveals a breach. Replaced with tracking language (Preferred: silent). Fallback: a contractual period no shorter than the longer of the statutory period and 3 years.]
94	ARTICLE XI — DOCUMENT RETENTION
95	Section 11.1 — Document Retention. The Parties shall not destroy, and shall retain for a minimum of seven (7) years following the issuance of the final Award (or, if applicable, the final appellate award under Section 8.4), all documents, materials, evidence, submissions, transcripts, orders, Awards, and other records produced, created, or exchanged during the arbitration. This obligation shall survive the termination of this Agreement and shall be binding upon each Party's officers, directors, employees, agents, and representatives.
96	[NOTE -- Classification: Required; destruction clauses are NOT ACCEPTABLE at any time period (Playbook s.20). Tier: Important. The destruction and certification obligation is deleted and replaced with a 7-year retention requirement. Fallback: return (not destruction) of produced documents to the producing Party, with all other materials retained for 7 years.]
97	
98	ARTICLE XII — GENERAL PROVISIONS
99	Section 12.1 — Notices. All notices, requests, demands, and other communications under this Agreement shall be delivered in the manner provided in Section 11.4 of the Co-Investment Agreement to the Parties at the addresses set forth therein or such other address as a Party may designate in writing from time to time in accordance with the provisions of the Co-Investment Agreement.
100	[NOTE -- No change proposed. Cross-reference to CIA Section 11.4 is not verified: the CIA is not in the data room.]
101	Section 12.2 — Entire Agreement. This Agreement constitutes the entire agreement between the Parties with respect to the subject matter hereof and supersedes all prior negotiations, representations, warranties, commitments, offers, and agreements (whether oral or written) with respect to the subject matter hereof.
102	Section 12.3 — Amendment and Waiver. This Agreement may not be amended, modified, or supplemented except by a written instrument signed by both Parties. No waiver of any provision of this Agreement shall be effective unless in writing signed by the waiving Party. No failure or delay by any Party in exercising any right, power, or privilege hereunder shall operate as a waiver thereof, nor shall any single or partial exercise thereof preclude any other or further exercise thereof or the exercise of any other right, power, or privilege.
103	Section 12.4 — Severability. If any provision of this Agreement is held to be invalid, illegal, or unenforceable in any respect, such invalidity, illegality, or unenforceability shall not affect any other provision of this Agreement, and this Agreement shall be construed as if such invalid, illegal, or unenforceable provision had never been contained herein. The Parties shall negotiate in good faith to replace any such invalid, illegal, or unenforceable provision with a valid, legal, and enforceable provision that, to the greatest extent possible, achieves the original intent and economic effect of the invalid provision.
104	Section 12.5 — Counterparts. This Agreement may be executed in counterparts, each of which shall be deemed an original, and all of which together shall constitute one and the same instrument. Execution and delivery of this Agreement by facsimile or electronic transmission (including in .pdf format) shall be deemed to be, and shall have the same legal effect as, execution and delivery of an original.
105	Section 12.6 — Relationship to Co-Investment Agreement. This Agreement is Exhibit F to and is incorporated into the Co-Investment Agreement. In the event of a conflict between the terms of this Agreement and the arbitration-related provisions of the Co-Investment Agreement, the terms of this Agreement shall control.
106	[NOTE -- The Co-Investment Agreement (not in the data room) must also be Delaware-governed and must not conflict with the arbitration provisions above (Playbook s.6). Confirm against the CIA before circulation.]
107	Section 12.7 — Survival. This Agreement shall survive the termination or expiration of the Co-Investment Agreement with respect to any Dispute arising prior to or upon such termination or expiration.
108	
109	[Signature Page Follows]
110	
111	IN WITNESS WHEREOF, the Parties have executed this Arbitration Agreement as of the date first written above.
112	WHITMORE CAPITAL FUND III LP
113	By: Whitmore Capital Partners LLC, its General Partner
114	By: ________
115	Name: ________
116	Title: ________
117	Date: ________
118	CASCADIAN GROWTH FUND LP
119	By: Cascadian Growth Management LLC, its General Partner
120	By: ________
121	Name: ________
122	Title: ________
123	Date: ________
124	
[ASSISTANT] The accepted view reads correctly: the waiver is gone and replaced by the carve-out, the panel and seat and governing law are switched, the expedited track, confidentiality, appellate, damages and retention clauses are in, and every notes paragraph appears. Next I'll confirm the delivered file parses through the reader and carries the tracked changes.
[ACTION] Bash {"command": "python3 scripts/read_doc.py output/redlined-arbitration-agreement.docx > /tmp/redline-scratch/delivered.txt 2>&1; echo \"exit=$?\"; wc -l /tmp/redline-scratch/delivered.txt; grep -c \"NOTE\" /tmp/redline-scratch/delivered.txt; grep -n \"ins\\|del\" /tmp/redline-scratch/delivered.txt | head -5; grep -n \"Section 6.1\\|Section 6.2 \" /tmp/redline-scratch/delivered.txt | head -4", "description": "Re-read delivered redline and confirm notes and changes"}
[OBSERVATION]
exit=0
     233 /tmp/redline-scratch/delivered.txt
31
1:[*\[PRIVILEGED & CONFIDENTIAL \-- Whitmore internal review draft. Bracketed notes cite the Whitmore Arbitration Playbook v3.0 (Nov. 15, 2024) and fallback positions. Delete all notes before any circulation to Cascadian or Pinnacle Winterhaven.\]*]{.insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}[]{.paragraph-insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}
41:\"[**ICC**]{.deletion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}[AAA]{.insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}\" means the [International]{.deletion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}[American]{.insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"} [Chamber]{.deletion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}[Arbitration]{.insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"} [of Commerce]{.deletion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}[Association]{.insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}.
43:[*\[NOTE \-- Classification: Required (Playbook s.2). Tier: Important. ICC is reserved for cross-border deals and may never administer a purely domestic U.S. transaction. All parties, the Target (Houston, TX) and the equity are U.S.-based. Fallback: JAMS Comprehensive Rules if Cascadian objects to AAA.\]*]{.insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}[]{.paragraph-insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}
45:\"[**ICC**]{.deletion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}[AAA]{.insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"} **Rules**\" means the [Rules of]{.deletion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}[Commercial]{.insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"} Arbitration[ Rules]{.insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"} of the [International Chamber of Commerce]{.deletion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}[AAA]{.insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"} in effect at the time of commencement of the arbitration.
47:[*\[NOTE \-- Classification: Preferred (Playbook s.2): AAA Commercial Rules, most current version as of submission. Conforming change.\]*]{.insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}[]{.paragraph-insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}
121:[**Section 6.1 --- Waiver of Court Relief.** The Parties hereby expressly waive any right to seek provisional or interim measures, including but not limited to temporary restraining orders, preliminary injunctions, attachments, or any other form of interim or conservatory relief, from any court of competent jurisdiction in connection with any Dispute subject to arbitration under this Agreement. All requests for provisional or interim measures shall be directed exclusively to the Arbitral Tribunal. The Parties acknowledge that this waiver is knowing, voluntary, and made in consideration of the mutual benefits of resolving all aspects of any Dispute through the arbitral process established herein.]{.deletion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}[]{.paragraph-deletion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}
123:[*\[NOTE \-- Classification: Required; waiver of court interim relief is NOT ACCEPTABLE (Playbook s.10). Tier: Critical. Deleted in full, with the carve-out in Section 6.2 substituted. R. Stadler (1/9/25) identifies this as non-negotiable. Any counter-proposal restricting court relief goes to the GC immediately.\]*]{.insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}[]{.paragraph-insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}
125:[**Section 6.2 --- Court Interim Relief Preserved.** Notwithstanding Sections 2.1 and 2.2, any Party may at any time before, during, or after the arbitration seek provisional, interim, conservatory, or injunctive measures, including temporary restraining orders, preliminary injunctions, attachments, and asset-freezing orders, from any court of competent jurisdiction. Seeking such relief shall not constitute a waiver of the right to arbitrate, is not inconsistent with this Agreement, and shall not be deemed a submission to the jurisdiction of such court for any purpose other than the relief sought.]{.insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}[]{.paragraph-insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}
129:[**Section 6.3 --- Emergency Arbitrator.** Before the Arbitral Tribunal is constituted, any Party may apply for emergency measures of protection under the AAA Optional Rules for Emergency Measures of Protection in effect at the time of the application. An emergency arbitrator order does not substitute for relief from a court under Section 6.2, and a Party may seek relief from a court under Section 6.2 whether or not an emergency arbitrator application has been made.]{.insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}[]{.paragraph-insertion author="Hargrove, Wynn & Calloway LLP" date="2025-01-01T00:00:00Z"}
[ASSISTANT] The delivered file parses, and the tracked insertions and deletions show up in it. Checking my own notes against the arithmetic, the expedited note's suggested fix is off. A hearing 21 days after appointment would leave only about 10 days for the award, so I'll change that to 14 days and rebuild.
[ACTION] Bash {"command": "python3 -I -c \"\nimport json\np='/tmp/redline-scratch/spec.json'\ns=json.load(open(p,encoding='utf-8'))\nn=0\nfor sec in ('edits','inserts','notes','deletes'):\n  for e in s.get(sec,[]):\n    if 'note' in e and 'about 21 days after appointment' in e['note']:\n      e['note']=e['note'].replace('about 21 days after appointment','about 14 days after appointment'); n+=1\njson.dump(s,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)\nprint('replaced',n)\n\" && python3 -I .claude/skills/redline-docx/scripts/tracked_redline.py documents/proposed-arbitration-agreement.docx /tmp/redline-scratch/spec.json output/redlined-arbitration-agreement.docx && python3 -I .claude/skills/redline-docx/scripts/check_redline.py documents/proposed-arbitration-agreement.docx output/redlined-arbitration-agreement.docx --accepted /tmp/redline-scratch/accepted.txt; echo \"exit=$?\"; grep -c \"^\\[NOTE\" /tmp/redline-scratch/accepted.txt", "description": "Correct the expedited hearing note and rebuild and recheck"}
[OBSERVATION]
replaced 1
wrote output/redlined-arbitration-agreement.docx: 24 edits, 1 deletes, 7 inserts, 38 notes, 412 revision marks
revisions: 253 insertions, 159 deletions
OK: reject-all text == original (78 paragraphs)
accepted view -> /tmp/redline-scratch/accepted.txt
exit=0
31
[ASSISTANT] The redline is rebuilt, passes the reject-all check, and carries 31 notes. Next, the cover memo.
[ACTION] Write {"file_path": "/tmp/redline-scratch/memo.md", "content": "**PRIVILEGED & CONFIDENTIAL -- ATTORNEY-CLIENT PRIVILEGED / ATTORNEY WORK PRODUCT**\n\n# Cover Memo: Markup of Proposed Arbitration Agreement (Exhibit F to Co-Investment Agreement)\n\n**To:** Rebecca Stadler, General Counsel, Whitmore Capital Partners LLC\n**From:** Hargrove, Wynn & Calloway LLP (draft for partner review, D. Ostrander)\n**Date:** [to be inserted on issue]\n**Re:** Vantage Specialty Chemicals / Cascadian Growth Fund LP co-investment; redline of Cascadian's proposed arbitration agreement\n\n**Deliverable:** `redlined-arbitration-agreement.docx` (tracked changes against Pinnacle Winterhaven's January 8 draft; 31 bracketed internal notes).\n\n## 1. Summary\n\n- Cascadian's form departs from the Whitmore Arbitration Playbook (v3.0, Nov. 15, 2024) on nearly every topic. We have marked up each departure.\n- All five Critical items are addressed: court interim relief (waiver deleted), three-member panel with selection mechanics, Delaware governing law, no shortening of limitations, and the class waiver. The expedited track (Rebecca Stadler's third priority) is also in the markup.\n- No Required position has been conceded. The markup offers no fallbacks in the body. Fallbacks appear only in the internal notes, for use if Cascadian objects.\n- Three points need a decision before the redline goes out (Section 5): the expedited timeline does not fit internally, the class waiver's wording conflicts with the consoli
[OBSERVATION]
The file /tmp/redline-scratch/memo.md has been updated successfully. (file state is current in your context — no need to Read it back)
[ACTION] Bash {"command": "pandoc /tmp/redline-scratch/memo.md -o output/markup-cover-memo.docx && python3 scripts/read_doc.py output/markup-cover-memo.docx > /tmp/redline-scratch/memo-check.txt 2>&1; echo \"exit=$?\"; wc -c output/markup-cover-memo.docx; grep -c \"|\" /tmp/redline-scratch/memo-check.txt; grep -n \"Critical\\|Important\\|Recommended\\|Open Issues\" /tmp/redline-scratch/memo-check.txt | head -12; ls -la output", "description": "Convert memo to docx with pandoc and verify tables"}
[OBSERVATION]
exit=0
   17121 output/markup-cover-memo.docx
0
12:- All five Critical items are addressed: court interim relief (waiver deleted), three-member panel with selection mechanics, Delaware governing law, no shortening of limitations, and the class waiver. The expedited track (Rebecca Stadler's third priority) is also in the markup.
25:  Expedited track tier                    Playbook §22 lists it as Recommended; §17 is Required; R. Stadler calls it "critical"                                                                             Classified Required; tier Critical (client instruction governs)
27:  Discovery (§8)                          §8 body says Required; §22 summary says Recommended                                                                                                               Treated as Required (specific body text governs); confirm with GC
38:Two axes are used throughout and kept separate: **Position** (Required / Preferred / Fallback, per the playbook) and **Tier** (Critical / Important / Recommended, per playbook §22, as adjusted by client instruction).
40:### 3.1 Critical
55:  6          Expedited track (new §5.4)        Absent                                       Sole arbitrator for capital call, drag-along, and buy-sell disputes. Appointment within 10 business days; hearing within 30 days of appointment; document production only (max 5 requests per side); final award within 45 days   Required (§17); tier Critical per R. Stadler        Award deadline up to 60 days, no longer. See Section 5, item 1.
60:### 3.2 Important
86:### 3.3 Recommended
91:  16         Arbitrator qualifications (§4.3)   Neutral and independent only               15 years PE/M&A/corporate finance; AAA National Roster; 5-year conflict lookback                                                       Required (§5 body); tier Recommended per §22   10 years, only with prior GC approval
93:  17         Discovery (§5.1)                   ICC Rules "without modification"           3 fact depositions per side (7 hours each); 15 document requests per side; 1 testifying expert per side; simultaneous expert reports   Required (§8 body); tier Recommended per §22   "Limited and proportional" language, with the deposition and expert caps as non-negotiable minimums
95:  18         Award timing and content (§8.1)    120 days, "best efforts"; reasoned award   90 days; detailed findings of fact and conclusions of law                                                                              Required (§18); tier Recommended per §22       Up to 120 days; findings and conclusions non-negotiable
105:## 5. Open Issues to Resolve Before Sending
total 152
drwxr-xr-x@ 4 me  staff    128 Oct 19 12:08 .
drwxr-xr-x@ 7 me  staff    224 Oct 19 12:01 ..
-rw-r--r--@ 1 me  staff  17121 Oct 19 12:08 markup-cover-memo.docx
-rw-r--r--@ 1 me  staff  54821 Oct 19 12:08 redlined-arbitration-agreement.docx
[ASSISTANT] I've produced both deliverables in `output/`: `redlined-arbitration-agreement.docx` and `markup-cover-memo.docx`. The redline is a tracked-changes markup of Cascadian's form with 31 bracketed notes, and the memo groups every change by priority tier.

**What the markup does**
- **Critical:** deletes the court interim-relief waiver and adds a court carve-out and AAA emergency-arbitrator provisions. Changes the sole arbitrator to a three-member panel with party appointments and a chair. Moves governing law from Washington to Delaware. Replaces the one-year limitations period with language that tracks the statute. Adds the class waiver, which the form omitted. Adds the 45-day expedited track for capital call, drag-along and buy-sell disputes.
- **Important:** ICC to AAA, Seattle to Atlanta, a confidentiality clause, a mutual damages waiver with a fraud carve-out, prevailing-party fee-shifting, consent-based joinder and consolidation, no document destruction with 7-year retention, and optional appellate arbitration for awards over $25M.
- **Recommended:** arbitrator qualifications, discovery caps, and the 90-day award with findings of fact and conclusions of law.

**Choices I made**
- Rebecca's emails govern where they conflict with the playbook. I treated the panel selection mechanics as Required (the playbook lists them as Preferred) and the expedited track as Critical (the playbook summary lists it as Recommended).
- Fallbacks appear only in the internal notes, not in the body of the redline.

**Decisions needed before this goes out**
1. **The expedited timeline does not fit.** A 10-business-day appointment, a hearing 30 days after appointment, and a 45-day award leave about one day for a reasoned award. The memo gives two fixes: shorten the hearing window to about 14 days after appointment, or take the 60-day fallback.
2. **The class waiver conflicts with consolidation.** The playbook's required wording bars "consolidated" proceedings, which would block even consented consolidation under §7.1.
3. **The Co-Investment Agreement is not in the data room.** Its governing law must also be Delaware, and its notice and arbitration cross-references are unverified.
4. **The playbook is internally inconsistent on discovery.** §8 says Required and §22 says Recommended. I treated it as Required; please confirm.
5. **The deadline conflicts.** The first email said Jan 11; the later emails say Jan 12.

**Caveats**
- The bracketed notes cite the playbook, fallbacks and GC-only positions. They must be stripped before anything goes to Pinnacle Winterhaven or Cascadian. I did not prepare a clean external version.
- The redline's revision timestamps use the script default of January 1, 2025. Reset them to the actual markup date before issue.
- The redline passed the reject-all check (rejecting every change restores the original text). I did not render it visually, and I have not opened it in Word.
- The memo's date is left as a placeholder.