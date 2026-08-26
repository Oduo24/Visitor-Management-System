import {
  useEffect,
  useState,
  type FormEvent,
} from "react";
 
import axios from "axios";
 
import {
  useMutation,
  useQuery,
} from "@tanstack/react-query";
 
import {
  useParams,
} from "react-router-dom";
 
import {
  completeVisitInvitation,
  getVisitInvitation,
} from "../../api/invitations.api";
 
 
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
 
 
export function PublicInvitationPage() {
 
  const {
    token,
  } = useParams();
 
 
  const [
    firstName,
    setFirstName,
  ] = useState("");
 
  const [
    middleName,
    setMiddleName,
  ] = useState("");
 
  const [
    lastName,
    setLastName,
  ] = useState("");
 
  const [
    phone,
    setPhone,
  ] = useState("");
 
  const [
    email,
    setEmail,
  ] = useState("");
 
  const [
    idNumber,
    setIdNumber,
  ] = useState("");
 
  const [
    passportNumber,
    setPassportNumber,
  ] = useState("");
 
  const [
    vehicleRegistration,
    setVehicleRegistration,
  ] = useState("");
 
  const [
    formError,
    setFormError,
  ] = useState<string | null>(
    null
  );
 
  const [
    completed,
    setCompleted,
  ] = useState(false);
 
 
  const invitationQuery =
    useQuery({
 
      queryKey: [
        "public-invitation",
        token,
      ],
 
      queryFn: () => {
 
        if (!token) {
          throw new Error(
            "Invitation token is missing."
          );
        }
 
        return getVisitInvitation(
          token
        );
      },
 
      enabled: Boolean(
        token
      ),
 
      retry: false,
    });
 
 
  useEffect(() => {
 
    const invitation =
      invitationQuery.data;
 
    if (!invitation) {
      return;
    }
 
    const visitor =
      invitation.visitor;
 
    setFirstName(
      visitor.first_name ?? ""
    );
 
    setMiddleName(
      visitor.middle_name ?? ""
    );
 
    setLastName(
      visitor.last_name ?? ""
    );
 
    setPhone(
      visitor.phone ?? ""
    );
 
    setEmail(
      visitor.email ?? ""
    );
 
    setIdNumber(
      visitor.id_number ?? ""
    );
 
    setPassportNumber(
      visitor.passport_number
      ?? ""
    );
 
    setVehicleRegistration(
      visitor.vehicle_registration
      ?? ""
    );
 
  }, [
    invitationQuery.data,
  ]);
 
 
  const completeMutation =
    useMutation({
 
      mutationFn: () => {
 
        if (!token) {
          throw new Error(
            "Invitation token is missing."
          );
        }
 
        return completeVisitInvitation(
          token,
          {
            first_name:
              firstName.trim(),
 
            middle_name:
              middleName.trim()
                || null,
 
            last_name:
              lastName.trim(),
 
            phone:
              phone.trim(),
 
            email:
              email.trim()
                || null,
 
            id_number:
              idNumber.trim()
                || null,
 
            passport_number:
              passportNumber.trim()
                || null,
 
            vehicle_registration:
              vehicleRegistration.trim()
                || null,
          }
        );
      },
 
 
      onSuccess: () => {
 
        setFormError(null);
 
        setCompleted(
          true
        );
      },
 
 
      onError: (error) => {
 
        setFormError(
          getErrorMessage(
            error,
            "Unable to complete invitation."
          )
        );
      },
 
    });
 
 
  function handleSubmit(
    event: FormEvent
  ) {
 
    event.preventDefault();
 
    setFormError(null);
 
 
    if (
      !firstName.trim()
      ||
      !lastName.trim()
      ||
      !phone.trim()
    ) {
 
      setFormError(
        "First name, last name and phone number are required."
      );
 
      return;
    }
 
 
    completeMutation.mutate();
  }
 
 
  if (
    invitationQuery.isLoading
  ) {
 
    return (
      <div className="public-page">
        <div className="public-card">
          Loading invitation...
        </div>
      </div>
    );
  }
 
 
  if (
    invitationQuery.isError
    ||
    !invitationQuery.data
  ) {
 
    return (
      <div className="public-page">
 
        <div className="public-card">
 
          <h1>
            Invitation unavailable
          </h1>
 
          <p className="page-error">
            {
              getErrorMessage(
                invitationQuery.error,
                "This invitation is invalid, expired, or no longer available."
              )
            }
          </p>
 
        </div>
 
      </div>
    );
  }
 
 
  if (completed) {
 
    return (
      <div className="public-page">
 
        <div className="public-card success-card">
 
          <h1>
            Details submitted
          </h1>
 
          <p>
            Your visitor information
            has been submitted
            successfully.
          </p>
 
          <p>
            Please keep your visitor
            code or invitation
            information available when
            you arrive.
          </p>
 
        </div>
 
      </div>
    );
  }
 
 
  const invitation =
    invitationQuery.data;
 
 
  return (
    <div className="public-page">
 
      <div className="public-card">
 
        <div className="public-heading">
 
          <h1>
            Visitor Invitation
          </h1>
 
          <p>
            Confirm and complete your
            visitor information.
          </p>
 
        </div>
 
 
        <section className="invitation-summary">
 
          <h2>
            Visit Details
          </h2>
 
 
          <SummaryRow
            label="Host"
            value={
              invitation.host
            }
          />
 
          <SummaryRow
            label="Site"
            value={
              invitation.site
            }
          />
 
          <SummaryRow
            label="Visit Type"
            value={
              invitation.visit_type
                .replaceAll(
                  "_",
                  " "
                )
            }
          />
 
          <SummaryRow
            label="Arrival"
            value={
              formatDate(
                invitation.expected_arrival
              )
            }
          />
 
          <SummaryRow
            label="Purpose"
            value={
              invitation.purpose
              ?? "-"
            }
          />
 
          <SummaryRow
            label="Invitation Expires"
            value={
              formatDate(
                invitation.expires_at
              )
            }
          />
 
        </section>
 
 
        <form
          onSubmit={
            handleSubmit
          }
        >
 
          <section className="invitation-form">
 
            <h2>
              Your Details
            </h2>
 
 
            <div className="form-grid">
 
              <FormInput
                label="First Name *"
                value={firstName}
                onChange={
                  setFirstName
                }
              />
 
              <FormInput
                label="Middle Name"
                value={middleName}
                onChange={
                  setMiddleName
                }
              />
 
              <FormInput
                label="Last Name *"
                value={lastName}
                onChange={
                  setLastName
                }
              />
 
              <FormInput
                label="Phone *"
                type="tel"
                value={phone}
                onChange={
                  setPhone
                }
              />
 
              <FormInput
                label="Email"
                type="email"
                value={email}
                onChange={
                  setEmail
                }
              />
 
              <FormInput
                label="ID Number"
                value={idNumber}
                onChange={
                  setIdNumber
                }
              />
 
              <FormInput
                label="Passport Number"
                value={
                  passportNumber
                }
                onChange={
                  setPassportNumber
                }
              />
 
              <FormInput
                label="Vehicle Registration"
                value={
                  vehicleRegistration
                }
                onChange={
                  setVehicleRegistration
                }
              />
 
            </div>
 
 
            {formError && (
 
              <div className="form-error">
                {formError}
              </div>
 
            )}
 
 
            <button
              type="submit"
              className="button public-submit"
              disabled={
                completeMutation.isPending
              }
            >
              {
                completeMutation.isPending
                  ? "Submitting..."
                  : "Submit Details"
              }
            </button>
 
          </section>
 
        </form>
 
      </div>
 
    </div>
  );
}
 
 
function SummaryRow({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
 
  return (
    <div className="summary-row">
 
      <span className="summary-label">
        {label}
      </span>
 
      <span>
        {value}
      </span>
 
    </div>
  );
}
 
 
function FormInput({
  label,
  value,
  type = "text",
  onChange,
}: {
  label: string;
  value: string;
  type?: string;
  onChange: (
    value: string
  ) => void;
}) {
 
  return (
    <div className="form-field">
 
      <label>
        {label}
      </label>
 
      <input
        type={type}
        value={value}
        onChange={(event) =>
          onChange(
            event.target.value
          )
        }
      />
 
    </div>
  );
}