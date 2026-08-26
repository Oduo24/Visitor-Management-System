import axios from "axios";
 
import {
  useQuery,
} from "@tanstack/react-query";
 
import {
  useParams,
} from "react-router-dom";
 
import {
  QRCodeSVG,
} from "qrcode.react";
 
import {
  getVisitorPass,
} from "../../api/visitorPass.api";
 
 
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
 
 
export function VisitorPassPage() {
 
  const {
    token,
  } = useParams();
 
 
  const {
    data: visitorPass,
    isLoading,
    isError,
    error,
  } = useQuery({
 
    queryKey: [
      "visitor-pass",
      token,
    ],
 
    queryFn: () => {
 
      if (!token) {
        throw new Error(
          "Visitor pass token is missing."
        );
      }
 
      return getVisitorPass(
        token
      );
    },
 
    enabled: Boolean(
      token
    ),
 
    retry: false,
  });
 
 
  if (isLoading) {
 
    return (
      <div className="visitor-pass-page">
        Loading visitor pass...
      </div>
    );
  }
 
 
  if (
    isError
    ||
    !visitorPass
  ) {
 
    let message =
      "This visitor pass is unavailable.";
 
    if (
      axios.isAxiosError(error)
    ) {
 
      message =
        error.response?.data
          ?.message
        ??
        message;
    }
 
    return (
      <div className="visitor-pass-page">
 
        <div className="pass-document">
 
          <h1>
            Visitor Pass Unavailable
          </h1>
 
          <p>
            {message}
          </p>
 
        </div>
 
      </div>
    );
  }
 
 
  return (
    <div className="visitor-pass-page">
 
      <div className="pass-actions">
 
        <button
          type="button"
          className="button"
          onClick={() =>
            window.print()
          }
        >
          Print / Save as PDF
        </button>
 
      </div>
 
 
      <main className="pass-document">
 
        <header className="pass-header">
 
          <div>
 
            <div className="pass-eyebrow">
              OFFICIAL VISITOR PASS
            </div>
 
            <h1>
              Visitor Invitation
            </h1>
 
            <p>
              Present this pass at
              reception on arrival.
            </p>
 
          </div>
 
 
          <div className="pass-status">
            {
              visitorPass.status
                .replaceAll(
                  "_",
                  " "
                )
            }
          </div>
 
        </header>
 
 
        <section className="pass-main">
 
          <div className="pass-information">
 
            <PassField
              label="Visitor"
              value={
                visitorPass.visitor_name
              }
            />
 
            <PassField
              label="Company"
              value={
                visitorPass.company
                ?? "-"
              }
            />
 
            <PassField
              label="Host"
              value={
                visitorPass.host
              }
            />
 
            <PassField
              label="Site"
              value={
                visitorPass.site
              }
            />
 
            <PassField
              label="Destination"
              value={
                visitorPass.destination
                ?? "-"
              }
            />
 
            <PassField
              label="Expected Arrival"
              value={
                formatDate(
                  visitorPass
                    .expected_arrival
                )
              }
            />
 
            <PassField
              label="Expected Departure"
              value={
                formatDate(
                  visitorPass
                    .expected_departure
                )
              }
            />
 
            <PassField
              label="Purpose"
              value={
                visitorPass.purpose
                ?? "-"
              }
            />
 
            <PassField
              label="Vehicle"
              value={
                visitorPass
                  .vehicle_registration
                ?? "-"
              }
            />
 
          </div>
 
 
          <aside className="pass-access">
 
            <div className="pass-qr">
 
              <QRCodeSVG
                value={
                  visitorPass.qr_token
                }
                size={210}
                level="M"
              />
 
            </div>
 
 
            <div className="visitor-code-label">
              VISITOR CODE
            </div>
 
            <div className="visitor-code-value">
              {
                visitorPass
                  .visitor_code
              }
            </div>
 
          </aside>
 
        </section>
 
 
        <footer className="pass-footer">
 
          <p>
            This pass is issued for the
            visit shown above and should
            be presented at reception.
          </p>
 
          <p>
            Generated{" "}
            {
              formatDate(
                visitorPass
                  .pass_generated_at
              )
            }
          </p>
 
        </footer>
 
      </main>
 
    </div>
  );
}
 
 
function PassField({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
 
  return (
    <div className="pass-field">
 
      <div className="pass-field-label">
        {label}
      </div>
 
      <div className="pass-field-value">
        {value}
      </div>
 
    </div>
  );
}