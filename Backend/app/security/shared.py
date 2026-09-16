from app.security.security_manager import SecurityManager


# =========================================================
# SHARED SECURITY MANAGER
# =========================================================
#
# AI Buddy के सभी API और Agent components इसी single
# SecurityManager instance को use करेंगे.
#
# इससे permissions, approvals और security state अलग-अलग
# instances में विभाजित नहीं होंगे.
# =========================================================

security_manager = SecurityManager()