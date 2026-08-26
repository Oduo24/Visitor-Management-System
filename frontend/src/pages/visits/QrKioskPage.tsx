import {
  useEffect,
  useRef,
  useState,
} from "react";
 
import axios from "axios";
 
import {
  useMutation,
} from "@tanstack/react-query";
 
import {
  Link,
} from "react-router-dom";
 
import {
  Html5Qrcode,
} from "html5-qrcode";
 
import type {
  Visit,
} from "../../types/visit";
 
import {
  checkInVisit,
  getVisitById,
  validateVisitQR,
} from "../../api/visits.api";
 
 
function formatDate(
  value: string | null | undefined
) {
 
  if (!value) {
    return "-";
  }
 
  return new Date(
    value
  ).toLocaleString();
}
 
 
function getErrorMessage(
  error: unknown,
  fallback: string
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
      fallback
    );
  }
 
  return fallback;
}
 
 
export function QrKioskPage() {
 
  const scannerRef =
    useRef<Html5Qrcode | null>(
      null
    );
 
  const scanLockedRef =
    useRef(false);
 
 
  const [
    cameraEnabled,
    setCameraEnabled,
  ] = useState(false);
 
  const [
    manualToken,
    setManualToken,
  ] = useState("");
 
  const [
    resolvedVisit,
    setResolvedVisit,
  ] = useState<Visit | null>(
    null
  );
 
  const [
    error,
    setError,
  ] = useState<string | null>(
    null
  );
 
  const [
    cameraError,
    setCameraError,
  ] = useState<string | null>(
    null
  );
 
 
  const validateMutation =
    useMutation({
 
      mutationFn: (
        token: string
      ) => {
 
        return validateVisitQR(
          token
        );
      },
 
      onSuccess: (
        visit
      ) => {
 
        setError(null);
 
        setResolvedVisit(
          visit
        );
      },
 
      onError: (
        mutationError
      ) => {
 
        setResolvedVisit(
          null
        );
 
        setError(
          getErrorMessage(
            mutationError,
            "Unable to validate QR code."
          )
        );
      },
 
    });
 
 
  const checkInMutation =
    useMutation({
 
      mutationFn: async () => {
 
        if (!resolvedVisit) {
          throw new Error(
            "No visit is selected."
          );
        }
 
        await checkInVisit(
          resolvedVisit.id
        );
 
        return getVisitById(
          resolvedVisit.id
        );
      },
 
      onSuccess: (
        visit
      ) => {
 
        setError(null);
 
        setResolvedVisit(
          visit
        );
      },
 
      onError: (
        mutationError
      ) => {
 
        setError(
          getErrorMessage(
            mutationError,
            "Unable to check visitor in."
          )
        );
      },
 
    });
 
 
  useEffect(() => {
 
    if (!cameraEnabled) {
      return;
    }
 
    let disposed = false;
 
    const scanner =
      new Html5Qrcode(
        "qr-reader"
      );
 
    scannerRef.current =
      scanner;
 
 
    scanner.start(
      {
        facingMode:
          "environment",
      },
 
      {
        fps: 10,
 
        qrbox: {
          width: 250,
          height: 250,
        },
      },
 
      (decodedText) => {
 
        if (
          scanLockedRef.current
        ) {
          return;
        }
 
        scanLockedRef.current =
          true;
 
        setManualToken(
          decodedText
        );
 
        setCameraEnabled(
          false
        );
 
        validateMutation.mutate(
          decodedText
        );
      },
 
      () => {
        // Ignore ordinary frame
        // decode failures.
      }
    ).catch(
      (scannerError) => {
 
        if (disposed) {
          return;
        }
 
        console.error(
          scannerError
        );
 
        setCameraError(
          "Unable to access the camera. Check browser camera permissions."
        );
 
        setCameraEnabled(
          false
        );
      }
    );
 
 
    return () => {
 
      disposed = true;
 
      const activeScanner =
        scannerRef.current;
 
      scannerRef.current =
        null;
 
      if (!activeScanner) {
        return;
      }
 
      activeScanner
        .stop()
        .catch(() => {
          // Scanner may already
          // have stopped.
        })
        .finally(() => {
 
          try {
            activeScanner.clear();
          } catch {
            // Nothing else required.
          }
 
        });
    };
 
  }, [
    cameraEnabled,
  ]);
 
 
  function handleManualValidation() {
 
    const token =
      manualToken.trim();
 
    setError(null);
 
 
    if (!token) {
 
      setError(
        "Enter or scan a QR token."
      );
 
      return;
    }
 
 
    validateMutation.mutate(
      token
    );
  }
 
 
  function handleStartCamera() {
 
    setCameraError(null);
    setError(null);
 
    scanLockedRef.current =
      false;
 
    setCameraEnabled(
      true
    );
  }
 
 
  function handleReset() {
 
    setCameraEnabled(
      false
    );
 
    scanLockedRef.current =
      false;
 
    setManualToken("");
    setResolvedVisit(null);
    setError(null);
    setCameraError(null);
  }
 
 
  const canCheckIn =
    resolvedVisit?.status
      === "APPROVED"
    &&
    Boolean(
      resolvedVisit.badge_number
    );
 
 
  return (
    <div className="page">
 
      <div className="page-heading">
 
        <div>
 
          <h1>
            QR Kiosk
          </h1>
 
          <p>
            Scan a visitor pass to
            validate the visit and
            complete reception
            check-in.
          </p>
 
        </div>
 
 
        {resolvedVisit && (
 
          <button
            type="button"
            className="button"
            onClick={
              handleReset
            }
          >
            Scan Next Visitor
          </button>
 
        )}
 
      </div>
 
 
      {!resolvedVisit && (
 
        <div className="kiosk-grid">
 
          <section className="detail-card">
 
            <h2>
              Camera Scanner
            </h2>
 
 
            {!cameraEnabled && (
 
              <button
                type="button"
                className="button"
                onClick={
                  handleStartCamera
                }
              >
                Start Camera
              </button>
 
            )}
 
 
            {cameraEnabled && (
 
              <div
                id="qr-reader"
                className="qr-reader"
              />
 
            )}
 
 
            {cameraError && (
 
              <div className="form-error">
                {cameraError}
              </div>
 
            )}
 
          </section>
 
 
          <section className="detail-card">
 
            <h2>
              Manual QR Validation
            </h2>
 
            <p className="form-help">
              Use this for testing or
              when a camera is not
              available.
            </p>
 
 
            <input
              type="text"
              value={
                manualToken
              }
              placeholder="Paste QR token"
              onChange={(event) => {
 
                setManualToken(
                  event.target.value
                );
 
                setError(null);
              }}
              onKeyDown={(event) => {
 
                if (
                  event.key
                  === "Enter"
                ) {
                  handleManualValidation();
                }
              }}
            />
 
 
            <button
              type="button"
              className="button kiosk-validate-button"
              disabled={
                validateMutation
                  .isPending
              }
              onClick={
                handleManualValidation
              }
            >
              {
                validateMutation
                  .isPending
                  ? "Validating..."
                  : "Validate QR"
              }
            </button>
 
          </section>
 
        </div>
 
      )}
 
 
      {error && (
 
        <div className="form-error kiosk-error">
          {error}
        </div>
 
      )}
 
 
      {resolvedVisit && (
 
        <section className="kiosk-result">
 
          <div className="kiosk-result-header">
 
            <div>
 
              <div className="kiosk-valid-label">
                QR VALID
              </div>
 
              <h2>
                {
                  resolvedVisit
                    .visitor_name
                }
              </h2>
 
            </div>
 
 
            <div className="status-badge">
              {
                resolvedVisit.status
                  .replaceAll(
                    "_",
                    " "
                  )
              }
            </div>
 
          </div>
 
 
          <div className="kiosk-details">
 
            <KioskDetail
              label="Visitor Code"
              value={
                resolvedVisit
                  .visitor_code
                ?? "-"
              }
            />
 
            <KioskDetail
              label="Host"
              value={
                resolvedVisit
                  .host_name
                ?? "-"
              }
            />
 
            <KioskDetail
              label="Site"
              value={
                resolvedVisit
                  .site_name
                ?? "-"
              }
            />
 
            <KioskDetail
              label="Destination"
              value={
                resolvedVisit
                  .destination_name
                ?? "-"
              }
            />
 
            <KioskDetail
              label="Expected Arrival"
              value={
                formatDate(
                  resolvedVisit
                    .expected_arrival
                )
              }
            />
 
            <KioskDetail
              label="Badge"
              value={
                resolvedVisit
                  .badge_number
                ?? "Not issued"
              }
            />
 
            <KioskDetail
              label="Checked In"
              value={
                formatDate(
                  resolvedVisit
                    .checked_in_at
                )
              }
            />
 
          </div>
 
 
          <div className="kiosk-actions">
 
            {canCheckIn && (
 
              <button
                type="button"
                className="button"
                disabled={
                  checkInMutation
                    .isPending
                }
                onClick={() => {
 
                  const confirmed =
                    window.confirm(
                      `Check ${
                        resolvedVisit
                          .visitor_name
                      } in?`
                    );
 
                  if (confirmed) {
                    checkInMutation
                      .mutate();
                  }
                }}
              >
                {
                  checkInMutation
                    .isPending
                    ? "Checking In..."
                    : "Check Visitor In"
                }
              </button>
 
            )}
 
 
            {
              resolvedVisit.status
                === "APPROVED"
              &&
              !resolvedVisit.badge_number
              && (
 
                <div className="kiosk-warning">
 
                  <strong>
                    Badge required
                  </strong>
 
                  <p>
                    This visit is
                    approved, but a badge
                    must be issued before
                    check-in.
                  </p>
 
                  <Link
                    to={
                      `/visits/${
                        resolvedVisit.id
                      }`
                    }
                  >
                    Open Visit
                  </Link>
 
                </div>
 
              )
            }
 
 
            {
              resolvedVisit.status
                === "CHECKED_IN"
              && (
 
                <div className="kiosk-success">
 
                  Visitor checked in
                  successfully.
 
                  <div>
                    {
                      formatDate(
                        resolvedVisit
                          .checked_in_at
                      )
                    }
                  </div>
 
                </div>
 
              )
            }
 
 
            {
              resolvedVisit.status
                === "CHECKED_OUT"
              && (
 
                <div className="kiosk-info">
                  This visit has already
                  been completed.
                </div>
 
              )
            }
 
 
            <Link
              to={
                `/visits/${
                  resolvedVisit.id
                }`
              }
            >
              View Full Visit
            </Link>
 
          </div>
 
        </section>
 
      )}
 
    </div>
  );
}
 
 
function KioskDetail({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
 
  return (
    <div className="kiosk-detail">
 
      <div className="kiosk-detail-label">
        {label}
      </div>
 
      <div className="kiosk-detail-value">
        {value}
      </div>
 
    </div>
  );
}