# ScamShield System Architecture

**INNOV12 Competition | Team OBSIDIAN**  
*Track: Cyber & Digital Trust (Primary) / AI & GenAI (Supporting)*  
*Team Members: Soham Mitra, Khyati K Doshi, Srinistha Biswas*  

---

## Architectural Principles

1. **Grounded Explainability:** No fabricated or plausible-sounding synthetic reasoning. Every output flag must be backed by a verbatim substring quote from the input or an exact mathematical feature weight ($w_i \cdot x_i$) from the Logistic Regression model.
2. **Deterministic Safety Floor:** Critical threat patterns (UPI PIN harvesting, emergency payment demands) trigger a minimum risk tier regardless of linguistic obfuscation.
3. **Decoupled Brand Configuration:** High-risk brand targets for URL spoofing are configured externally via `app/config/trusted_brands.json`.
4. **Dual Persistence Layer:** PostgreSQL primary with zero-config SQLite local fallback for resilient development and evaluation.
