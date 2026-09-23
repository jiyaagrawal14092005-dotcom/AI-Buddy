import {
    ShieldCheck,
    Mail,
    CheckCircle2,
    XCircle,
} from "lucide-react";


function ApprovalRequest({
    approvalId,
    action = "email",
    details = {},
    onApproved,
    onRejected,
    loading = false,
}) {

    const recipient =
        details?.recipient ||
        details?.parameters?.recipient ||
        "";

    const subject =
        details?.subject ||
        details?.parameters?.subject ||
        "";

    const message =
        details?.message ||
        details?.parameters?.message ||
        "";


    const handleApprove = () => {

        if (
            !approvalId ||
            loading
        ) {
            return;
        }

        if (onApproved) {
            onApproved();
        }
    };


    const handleReject = () => {

        if (
            !approvalId ||
            loading
        ) {
            return;
        }

        if (onRejected) {
            onRejected();
        }
    };


    return (

        <div className="approval-request-card">

            {/* ==========================================
                HEADER
            ========================================== */}

            <div className="approval-request-header">

                <div className="approval-request-icon">

                    <ShieldCheck size={20} />

                </div>


                <div>

                    <span className="approval-request-label">
                        SECURITY APPROVAL
                    </span>

                    <h3>
                        Zarvis needs your approval
                    </h3>

                </div>

            </div>


            {/* ==========================================
                BODY
            ========================================== */}

            <div className="approval-request-body">

                <p>
                    This action requires your permission
                    before Zarvis can execute it.
                </p>


                {/* ======================================
                    EMAIL DETAILS
                ====================================== */}

                {action === "email" && (

                    <div className="approval-email-details">

                        <div className="approval-detail-row">

                            <span>

                                <Mail size={14} />

                                Recipient

                            </span>


                            <strong>

                                {recipient ||
                                    "Not specified"}

                            </strong>

                        </div>


                        <div className="approval-detail-row">

                            <span>
                                Subject
                            </span>


                            <strong>

                                {subject ||
                                    "No subject"}

                            </strong>

                        </div>


                        <div className="approval-message">

                            <span>
                                Message
                            </span>


                            <p>

                                {message ||
                                    "No message"}

                            </p>

                        </div>

                    </div>

                )}


                {/* ======================================
                    GENERIC ACTION
                ====================================== */}

                {action !== "email" && (

                    <div className="approval-generic-details">

                        <span>
                            Requested action
                        </span>


                        <strong>
                            Zarvis wants to perform
                            this action.
                        </strong>

                    </div>

                )}

            </div>


            {/* ==========================================
                ACTION BUTTONS
            ========================================== */}

            <div className="approval-request-actions">

                <button
                    type="button"
                    className="approval-reject-button"
                    onClick={handleReject}
                    disabled={loading}
                >

                    <XCircle size={16} />

                    {loading
                        ? "Processing..."
                        : "Reject"}

                </button>


                <button
                    type="button"
                    className="approval-approve-button"
                    onClick={handleApprove}
                    disabled={loading}
                >

                    <CheckCircle2 size={16} />

                    {loading
                        ? "Processing..."
                        : "Approve & Continue"}

                </button>

            </div>

        </div>
    );
}


export default ApprovalRequest;