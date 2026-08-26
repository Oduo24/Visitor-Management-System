import {
  useQuery,
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";

import {
  QRCodeSVG,
} from "qrcode.react";
 
import {
  Link,
  useParams,
} from "react-router-dom";
 
import {
  getVisitById,
  updateVisitApproval,
  issueVisitBadge,
  generateVisitQR,
  checkInVisit,
  checkOutVisit,

} from "../../api/visits.api";

import {
  createVisitInvitation,
} from "../../api/invitations.api";
 
import {
  StatusBadge,
} from "../../components/common/StatusBadge";

import {
  useState,
} from "react";
 
import axios from "axios";
 
 
 
function formatDate(
  value: string | null
) {
 
  if (!value) {
    return "-";
  }
 
  return new Date(
    value
  ).toLocaleString();
}
 
 
export function VisitDetailPage() {
 
  const {
    visitId,
  } = useParams();

  const queryClient =
    useQueryClient();
  
  const [
    approvalNotes,
    setApprovalNotes,
  ] = useState("");
  
  const [
    actionError,
    setActionError,
  ] = useState<string | null>(
    null
  );

  const [
    badgeError,
    setBadgeError,
  ] = useState<string | null>(
    null
  );

  const [
    qrError,
    setQrError,
  ] = useState<string | null>(
    null
  );

  const [
    checkInError,
    setCheckInError,
  ] = useState<string | null>(
    null
  );


  const [
    checkOutError,
    setCheckOutError,
  ] = useState<string | null>(
    null
  );

  const [
    invitationError,
    setInvitationError,
  ] = useState<string | null>(
    null
  );
  
  const [
    invitationCreated,
    setInvitationCreated,
  ] = useState(false);

 
  const {
    data: visit,
    isLoading,
    isError,
  } = useQuery({
    queryKey: [
      "visit",
      visitId,
    ],
 
    queryFn: () =>
      getVisitById(
        visitId!
      ),
 
    enabled: Boolean(
      visitId
    ),
  });


  const approvalMutation =
  useMutation({
 
    mutationFn: (
      approved: boolean
    ) => {
 
      if (!visitId) {
        throw new Error(
          "Visit ID is missing."
        );
      }
 
      const notes =
        approvalNotes.trim();
 
      return updateVisitApproval(
        visitId,
        {
          approved,
 
          ...(notes && {
            notes,
          }),
        }
      );
    },
 
 
    onSuccess: async () => {
 
      setApprovalNotes("");
      setActionError(null);
 
      await Promise.all([
        queryClient.invalidateQueries({
          queryKey: [
            "visit",
            visitId,
          ],
        }),
 
        queryClient.invalidateQueries({
          queryKey: [
            "visits",
          ],
        }),
      ]);
    },
 
 
    onError: (error) => {
 
      if (
        axios.isAxiosError(error)
      ) {
 
        const data =
          error.response?.data as {
            message?: string;
            error?: string;
          } | undefined;
 
        setActionError(
          data?.message
          ??
          data?.error
          ??
          "Unable to update visit approval."
        );
 
        return;
      }
 
      setActionError(
        "Unable to update visit approval."
      );
    },
 
  });


  const badgeMutation =
  useMutation({
 
    mutationFn: () => {
 
      if (!visitId) {
        throw new Error(
          "Visit ID is missing."
        );
      }
 
      return issueVisitBadge(
        visitId
      );
    },
 
 
    onSuccess: async () => {
 
      setBadgeError(null);
 
      await Promise.all([
 
        queryClient.invalidateQueries({
          queryKey: [
            "visit",
            visitId,
          ],
        }),
 
        queryClient.invalidateQueries({
          queryKey: [
            "visits",
          ],
        }),
 
      ]);
    },
 
 
    onError: (error) => {
 
      if (
        axios.isAxiosError(error)
      ) {
 
        const data =
          error.response?.data as {
            message?: string;
            error?: string;
          } | undefined;
 
        setBadgeError(
          data?.message
          ??
          data?.error
          ??
          "Unable to issue badge."
        );
 
        return;
      }
 
      setBadgeError(
        "Unable to issue badge."
      );
    },
 
  });


  const qrMutation =
  useMutation({
 
    mutationFn: () => {
 
      if (!visitId) {
        throw new Error(
          "Visit ID is missing."
        );
      }
 
      return generateVisitQR(
        visitId
      );
    },
 
 
    onSuccess: async () => {
 
      setQrError(null);
 
      await Promise.all([
 
        queryClient.invalidateQueries({
          queryKey: [
            "visit",
            visitId,
          ],
        }),
 
        queryClient.invalidateQueries({
          queryKey: [
            "visits",
          ],
        }),
 
      ]);
    },
 
 
    onError: (error) => {
 
      if (
        axios.isAxiosError(error)
      ) {
 
        const data =
          error.response?.data as {
            message?: string;
            error?: string;
          } | undefined;
 
        setQrError(
          data?.message
          ??
          data?.error
          ??
          "Unable to generate QR code."
        );
 
        return;
      }
 
      setQrError(
        "Unable to generate QR code."
      );
    },
 
  });


  const checkInMutation =
  useMutation({
 
    mutationFn: () => {
 
      if (!visitId) {
        throw new Error(
          "Visit ID is missing."
        );
      }
 
      return checkInVisit(
        visitId
      );
    },
 
 
    onSuccess: async () => {
 
      setCheckInError(null);
 
      await Promise.all([
 
        queryClient.invalidateQueries({
          queryKey: [
            "visit",
            visitId,
          ],
        }),
 
        queryClient.invalidateQueries({
          queryKey: [
            "visits",
          ],
        }),
 
      ]);
    },
 
 
    onError: (error) => {
 
      if (
        axios.isAxiosError(error)
      ) {
 
        const data =
          error.response?.data as {
            message?: string;
            error?: string;
          } | undefined;
 
        setCheckInError(
          data?.message
          ??
          data?.error
          ??
          "Unable to check visitor in."
        );
 
        return;
      }
 
      setCheckInError(
        "Unable to check visitor in."
      );
    },
 
  });

  const checkOutMutation =
  useMutation({
 
    mutationFn: () => {
 
      if (!visitId) {
        throw new Error(
          "Visit ID is missing."
        );
      }
 
      return checkOutVisit(
        visitId
      );
    },
 
 
    onSuccess: async () => {
 
      setCheckOutError(null);
 
      await Promise.all([
 
        queryClient.invalidateQueries({
          queryKey: [
            "visit",
            visitId,
          ],
        }),
 
        queryClient.invalidateQueries({
          queryKey: [
            "visits",
          ],
        }),
 
      ]);
    },
 
 
    onError: (error) => {
 
      if (
        axios.isAxiosError(error)
      ) {
 
        const data =
          error.response?.data as {
            message?: string;
            error?: string;
          } | undefined;
 
        setCheckOutError(
          data?.message
          ??
          data?.error
          ??
          "Unable to check visitor out."
        );
 
        return;
      }
 
      setCheckOutError(
        "Unable to check visitor out."
      );
    },
 
  });


  const invitationMutation =
    useMutation({
  
      mutationFn: () => {
  
        if (!visitId) {
          throw new Error(
            "Visit ID is missing."
          );
        }
  
        return createVisitInvitation(
          visitId
        );
      },
  
  
      onSuccess: () => {
  
        setInvitationError(null);
  
        setInvitationCreated(
          true
        );
      },
  
  
      onError: (error) => {
  
        setInvitationError(
          getInvitationError(
            error
          )
        );
      },
  
    });
 
 
  if (isLoading) {
    return (
      <div>
        Loading visit...
      </div>
    );
  }
 
 
  if (
    isError
    || !visit
  ) {
    return (
      <div className="page-error">
        Unable to load visit.
      </div>
    );
  }
 
 
  return (
    <div>
 
      <div className="page-heading">
 
        <div>
 
          <Link
            to="/visits"
            className="back-link"
          >
            ← Back to Visits
          </Link>
 
          <h1>
            Visit Details
          </h1>
 
        </div>
 
        <StatusBadge
          status={visit.status}
        />
 
      </div>
 
 
      <div className="details-grid">
 
        <section className="detail-card">
 
          <h2>
            Visit
          </h2>
 
          <Detail
            label="Visit Type"
            value={
              visit.visit_type
            }
          />
 
          <Detail
            label="Purpose"
            value={
              visit.purpose
            }
          />
 
          <Detail
            label="Expected Arrival"
            value={
              formatDate(
                visit.expected_arrival
              )
            }
          />
 
          <Detail
            label="Expected Departure"
            value={
              formatDate(
                visit.expected_departure
              )
            }
          />
 
        </section>
 
 
        <section className="detail-card">
 
          <h2>
            Access
          </h2>
 
          <Detail
            label="Visitor Code"
            value={
              visit.visitor_code
            }
          />
 
          <Detail
            label="Badge"
            value={
              visit.badge_number
            }
          />
 
          <Detail
            label="QR Generated"
            value={
              formatDate(
                visit.qr_generated_at
              )
            }
          />
 
        </section>
 
 
        <section className="detail-card">
 
          <h2>
            Lifecycle
          </h2>
 
          {visit.status === "APPROVED" && (
            <Detail
              label="Approved"
              value={
                formatDate(
                  visit.approved_at
                )
              }
            />
          )}

          {visit.status === "REJECTED" && (
            <Detail
              label="Rejected"
              value={
                formatDate(
                  visit.rejected_at
                )
              }
            />
          )}
 
          <Detail
            label="Checked In"
            value={
              formatDate(
                visit.checked_in_at
              )
            }
          />
 
          <Detail
            label="Checked Out"
            value={
              formatDate(
                visit.checked_out_at
              )
            }
          />
 
        </section>
 
 
        <section className="detail-card">
 
          <h2>
            People and Location
          </h2>
 
          <Detail
            label="Visitor"
            value={
              visit.visitor_name
            }
          />
 
          <Detail
            label="Host"
            value={
              visit.host_name
            }
          />
 
          <Detail
            label="Site"
            value={
              visit.site_name
            }
          />
 
          <Detail
            label="Destination"
            value={
              visit.destination_name
            }
          />
 
        </section>

        {visit.status === "PENDING" && (
 
          <section className="detail-card lifecycle-card">
        
            <h2>
              Approval
            </h2>
        
            <p className="form-help">
              Approve or reject this visit.
              Notes are optional.
            </p>
        
        
            {actionError && (
              <div className="form-error">
                {actionError}
              </div>
            )}
        
        
            <div className="form-field">
        
              <label htmlFor="approvalNotes">
                Notes
              </label>
        
              <textarea
                id="approvalNotes"
                rows={3}
                value={approvalNotes}
                onChange={(event) =>
                  setApprovalNotes(
                    event.target.value
                  )
                }
                disabled={
                  approvalMutation.isPending
                }
                placeholder={
                  "Optional approval or rejection notes"
                }
              />
        
            </div>
        
        
            <div className="approval-actions">
        
              <button
                type="button"
                className="button approve-button"
                disabled={
                  approvalMutation.isPending
                }
                onClick={() => {
        
                  const confirmed =
                    window.confirm(
                      "Approve this visit?"
                    );
        
                  if (confirmed) {
                    approvalMutation.mutate(
                      true
                    );
                  }
                }}
              >
                {
                  approvalMutation.isPending
                    ? "Processing..."
                    : "Approve"
                }
              </button>
        
        
              <button
                type="button"
                className="button reject-button"
                disabled={
                  approvalMutation.isPending
                }
                onClick={() => {
        
                  const confirmed =
                    window.confirm(
                      "Reject this visit?"
                    );
        
                  if (confirmed) {
                    approvalMutation.mutate(
                      false
                    );
                  }
                }}
              >
                Reject
              </button>
        
            </div>
        
          </section>
        
        )}

        {visit.status === "APPROVED"
          &&
          !visit.badge_number
          && (
        
            <section className="detail-card lifecycle-card">
        
              <h2>
                Badge
              </h2>
        
              <p className="form-help">
                Issue an access badge for
                this approved visit.
              </p>
        
        
              {badgeError && (
                <div className="form-error">
                  {badgeError}
                </div>
              )}
        
        
              <button
                type="button"
                className="button"
                disabled={
                  badgeMutation.isPending
                }
                onClick={() => {
        
                  const confirmed =
                    window.confirm(
                      "Issue a badge for this visit?"
                    );
        
                  if (confirmed) {
                    badgeMutation.mutate();
                  }
                }}
              >
                {
                  badgeMutation.isPending
                    ? "Issuing Badge..."
                    : "Issue Badge"
                }
              </button>
        
            </section>
        
        )}

        {visit.status === "APPROVED"
          &&
          !visit.qr_token
          && (
        
            <section className="detail-card lifecycle-card">
        
              <h2>
                QR Code
              </h2>
        
              <p className="form-help">
                Generate a QR code for this
                approved visit.
              </p>
        
        
              {qrError && (
                <div className="form-error">
                  {qrError}
                </div>
              )}
        
        
              <button
                type="button"
                className="button"
                disabled={
                  qrMutation.isPending
                }
                onClick={() => {
        
                  const confirmed =
                    window.confirm(
                      "Generate QR code for this visit?"
                    );
        
                  if (confirmed) {
                    qrMutation.mutate();
                  }
                }}
              >
                {
                  qrMutation.isPending
                    ? "Generating QR..."
                    : "Generate QR"
                }
              </button>
        
            </section>
        
        )}

        {visit.qr_token && (
 
          <section className="detail-card lifecycle-card">
        
            <h2>
              QR Code
            </h2>
        
            <div className="qr-container">
        
              <QRCodeSVG
                value={visit.qr_token}
                size={220}
                level="M"
              />
        
              <div className="qr-details">
        
                <p>
                  Present this QR code at
                  reception for verification.
                </p>
        
                <Detail
                  label="Generated"
                  value={
                    formatDate(
                      visit.qr_generated_at
                    )
                  }
                />
        
              </div>
        
            </div>
        
          </section>
        
        )}

        {visit.status === "APPROVED"
          &&
          visit.badge_number
          && (
        
            <section className="detail-card lifecycle-card">
        
              <h2>
                Check-in
              </h2>
        
              <p className="form-help">
                Confirm that the visitor has
                arrived and check them in.
              </p>
        
        
              {checkInError && (
                <div className="form-error">
                  {checkInError}
                </div>
              )}
        
        
              <button
                type="button"
                className="button"
                disabled={
                  checkInMutation.isPending
                }
                onClick={() => {
        
                  const confirmed =
                    window.confirm(
                      "Check this visitor in?"
                    );
        
                  if (confirmed) {
                    checkInMutation.mutate();
                  }
                }}
              >
                {
                  checkInMutation.isPending
                    ? "Checking In..."
                    : "Check In"
                }
              </button>
        
            </section>
        
        )}

        {visit.status === "CHECKED_IN" && (
 
          <section className="detail-card lifecycle-card">
        
            <h2>
              Check-out
            </h2>
        
            <p className="form-help">
              Confirm that the visitor is
              leaving the premises.
            </p>
        
        
            {checkOutError && (
              <div className="form-error">
                {checkOutError}
              </div>
            )}
        
        
            <button
              type="button"
              className="button"
              disabled={
                checkOutMutation.isPending
              }
              onClick={() => {
        
                const confirmed =
                  window.confirm(
                    "Check this visitor out?"
                  );
        
                if (confirmed) {
                  checkOutMutation.mutate();
                }
              }}
            >
              {
                checkOutMutation.isPending
                  ? "Checking Out..."
                  : "Check Out"
              }
            </button>
        
          </section>
        
        )}

        {visit.visit_type === "PREBOOKED"
          &&
          (
            visit.status === "PENDING"
            ||
            visit.status === "APPROVED"
          )
          && (
        
            <section className="detail-card lifecycle-card">
        
              <h2>
                Visitor Invitation
              </h2>
        
        
              {invitationCreated ? (
        
                <p>
                  Invitation created successfully.
                  The visitor notification has been
                  triggered.
                </p>
        
              ) : (
        
                <>
        
                  <p className="form-help">
                    Send the visitor a link to
                    confirm and complete their
                    information before arrival.
                  </p>
        
        
                  {invitationError && (
        
                    <div className="form-error">
                      {invitationError}
                    </div>
        
                  )}
        
        
                  <button
                    type="button"
                    className="button"
                    disabled={
                      invitationMutation.isPending
                    }
                    onClick={() => {
        
                      const confirmed =
                        window.confirm(
                          "Create and send this visitor invitation?"
                        );
        
                      if (confirmed) {
                        invitationMutation.mutate();
                      }
                    }}
                  >
                    {
                      invitationMutation.isPending
                        ? "Creating Invitation..."
                        : "Send Invitation"
                    }
                  </button>
        
                </>
        
              )}
        
            </section>
        
        )}
      
 
      </div>
 
    </div>
  );
}
 
 
function Detail({
  label,
  value,
}: {
  label: string;
  value: string | null;
}) {
 
  return (
    <div className="detail-row">
 
      <div className="detail-label">
        {label}
      </div>
 
      <div className="detail-value">
        {value || "-"}
      </div>
 
    </div>
  );
}

function getInvitationError(
    error: unknown
  ) {
  
    if (
      axios.isAxiosError(error)
    ) {
  
      const data =
        error.response?.data as {
          message?: string;
          error?: string;
        } | undefined;
  
      return (
        data?.message
        ??
        data?.error
        ??
        "Unable to create invitation."
      );
    }
  
    return (
      "Unable to create invitation."
    );
  }




