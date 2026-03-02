O4DB™ PROTOCOL SPECIFICATION LICENSE
Version 1.0 — February 2026
Protocol Version: v1.1.5

Copyright © 2026 Daniel Eduardo Placanica. All Rights Reserved.
Safe Creative Registration IDs: 2602184604821-4XTVN6 / 2602204641140-6FSX6N / 2603014734558-2D52RP
UODI v1.2 Safe Creative: 2602284718909-6XLBXF
Patent Status: O4DB™ Patent Pending — U.S. Patent App. No. 63/993,946 (USPTO)
Contact: daniel@o4db.org

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. PURPOSE

This document defines the terms under which the O4DB™ Protocol 
Specification ("the Specification") may be accessed, studied, and used.

The Specification is made public to facilitate technical review, 
interoperability analysis, academic research, and to establish 
documented prior art. Public availability does not constitute a 
waiver of any intellectual property rights.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2. PERMITTED USE — COMMUNITY TIER

You are granted a limited, non-exclusive, non-transferable,
revocable license to:

  a) Read, study, and analyze the Specification.

  b) Implement the protocol logic for private, non-commercial
     testing and academic research purposes only.

  c) Reference or cite the Specification in academic papers,
     technical articles, or public commentary, provided that
     proper attribution is given to the author and the
     Safe Creative Registration ID is included.

  d) Community Tier Production Use: Deploy and operate the
     reference relay implementation in a production environment
     at no charge, subject to a hard limit of fifty (50)
     completed settlement operations per calendar month.
     Exceeding this threshold in any calendar month constitutes
     a Commercial Use and requires a written Commercial License
     from the author. The relay enforces this limit automatically
     via the COMMUNITY_LIMIT guard in the settlement endpoint.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. PROHIBITED USE

The following actions are STRICTLY PROHIBITED without an explicit, 
written commercial license agreement from the author:

  a) Commercial Implementation: Using this protocol, in whole or 
     in part, to facilitate, process, or manage commercial 
     transactions in any production environment.

  b) Derivative Works (Commercial): Creating, distributing, or 
     licensing commercial software, platforms, or services that 
     utilize the logic, flow, or architecture described in this 
     Specification — regardless of whether the original terminology 
     (VCI, ARA, JIT, SPS, O4DB) is preserved or replaced with 
     alternative naming conventions — without a written Commercial 
     License from the author. Non-commercial implementations 
     compliant with the Community Tier limits in Section 2 are 
     expressly permitted.

  c) SaaS/PaaS Offering: Offering O4DB™-compatible or 
     functionally equivalent services or infrastructure as a 
     commercial product.

  d) Sublicensing: Granting third parties any rights to use, 
     implement, or build upon this Specification.

  e) Misrepresentation: Representing any implementation as 
     officially affiliated with, endorsed by, or certified by 
     the author without explicit written authorization.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3b. CERTIFIED INTEGRATOR PROGRAM

Third-party software developers may apply for Certified Integrator
status to build and commercialize integration modules connecting
O4DB™ to external systems (ERP connectors, middleware adapters,
legacy system bridges, etc.) subject to the following conditions:

  a) The integration module must not modify the core protocol logic,
     cryptographic mechanisms, or settlement state machine.

  b) The integration module must preserve all O4DB™ trademark
     attributions and the Certified Integrator designation.

  c) The Certified Integrator may charge independently for their
     connector; however, end users of the connector remain subject
     to the Community or Commercial Tier limits of this License
     based on their own settlement volume.

  d) Certification is granted in writing by the author and may be
     revoked if the integration module violates protocol integrity.

  e) Uncertified connectors that misrepresent themselves as
     O4DB™-compatible or certified are subject to Section 5
     (Termination) and applicable trademark enforcement.

Contact daniel@o4db.org for Certified Integrator inquiries.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4. INTELLECTUAL PROPERTY

  a) This Specification is protected by international copyright 
     laws and treaties.

  b) The underlying logic — including but not limited to the VCI 
     emission flow, ARA execution mechanism, JIT identity release, 
     and SPS enforcement model — is subject to a patent pending before the USPTO (U.S. Patent App. No. 63/993,946).

  c) Access to or use of this Specification does not grant any 
     implied license to any pending or future patents held by 
     the author.

  d) The name O4DB™, the acronyms VCI, ARA, JIT, and SPS as 
     defined herein, and the phrase "Only for Determined Buyers" 
     are claimed as trademarks of Daniel Eduardo Placanica. 
     Unauthorized commercial use of these marks is prohibited.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5. TERMINATION

This license terminates automatically and without notice if you 
violate any of its terms. Upon termination, you must immediately 
cease all use of the Specification and destroy any copies in 
your possession. The author reserves the right to pursue all 
available legal remedies for violations.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

6. DISCLAIMER OF WARRANTIES

This Specification is provided "as is" without warranty of any 
kind, express or implied. The author makes no representations 
regarding the completeness, accuracy, or fitness for any 
particular purpose of the Specification.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

7. LIMITATION OF LIABILITY

In no event shall the author be liable for any direct, indirect, 
incidental, special, or consequential damages arising from the 
use or inability to use this Specification, even if advised of 
the possibility of such damages.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

8. GOVERNING LAW

This license shall be governed by and construed in accordance 
with applicable international intellectual property law. Any 
disputes arising under this license shall be subject to the 
jurisdiction agreed upon in any subsequent commercial license 
agreement, or failing that, the jurisdiction of the author's 
country of residence.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

9. COMMERCIAL INQUIRIES

For commercial licensing, partnerships, or production-grade 
implementation rights, contact the author directly:

  Daniel Eduardo Placanica
  daniel@o4db.org

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

© 2026 Daniel Eduardo Placanica. All Rights Reserved.
Safe Creative Registration ID: 2602184604821-4XTVN6
