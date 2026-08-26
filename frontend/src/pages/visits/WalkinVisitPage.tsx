import {
  useState,
  type FormEvent,
} from "react";
 
import axios from "axios";
 
import {
  useMutation,
  useQuery,
} from "@tanstack/react-query";
 
import {
  Link,
  useNavigate,
} from "react-router-dom";
 
import {
  createWalkinVisit,
} from "../../api/visits.api";
 
import {
  createVisitor,
} from "../../api/visitors.api";
 
import {
  getVisitors,
  getHosts,
  getSites,
  getDestinations,
} from "../../api/lookups.api";
 
 
type VisitorMode =
  | "existing"
  | "new";
 
 
export function WalkinVisitPage() {
 
  const navigate = useNavigate();
 
  const [
    visitorMode,
    setVisitorMode,
  ] = useState<VisitorMode>(
    "new"
  );
 
  const [
    visitorId,
    setVisitorId,
  ] = useState("");
 
  const [
    hostId,
    setHostId,
  ] = useState("");
 
  const [
    siteId,
    setSiteId,
  ] = useState("");
 
  const [
    destinationId,
    setDestinationId,
  ] = useState("");
 
  const [
    firstName,
    setFirstName,
  ] = useState("");
 
  const [
    lastName,
    setLastName,
  ] = useState("");
 
  const [
    email,
    setEmail,
  ] = useState("");
 
  const [
    phone,
    setPhone,
  ] = useState("");
 
  const [
    company,
    setCompany,
  ] = useState("");
 
  const [
    nationality,
    setNationality,
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
    purpose,
    setPurpose,
  ] = useState("");
 
  const [
    notes,
    setNotes,
  ] = useState("");
 
  const [
    formError,
    setFormError,
  ] = useState<string | null>(
    null
  );
 
 
  const visitorsQuery = useQuery({
    queryKey: ["visitors"],
    queryFn: getVisitors,
  });
 
  const hostsQuery = useQuery({
    queryKey: ["hosts"],
    queryFn: getHosts,
  });
 
  const sitesQuery = useQuery({
    queryKey: ["sites"],
    queryFn: getSites,
  });
 
  const destinationsQuery = useQuery({
    queryKey: ["destinations"],
    queryFn: getDestinations,
  });
 
 
  const createMutation = useMutation({
 
    mutationFn: async () => {
 
      let resolvedVisitorId =
        visitorId;
 
 
      if (
        visitorMode === "new"
      ) {
 
        const visitor =
          await createVisitor({
 
            first_name:
              firstName.trim(),
 
            last_name:
              lastName.trim(),
 
            email:
              email.trim() || null,
 
            phone:
              phone.trim(),
 
            company:
              company.trim() || null,
 
            nationality:
              nationality.trim() || null,
 
            id_number:
              idNumber.trim() || null,
 
            passport_number:
              passportNumber.trim()
              || null,
 
            vehicle_registration:
              vehicleRegistration.trim()
              || null,
          });
 
        resolvedVisitorId =
          visitor.id;
      }
 
 
      const payload = {
        visitor_id: resolvedVisitorId,
        host_id: hostId,
        site_id: siteId,
        destination_id: destinationId,

        ...(purpose.trim() && {
            purpose: purpose.trim(),
        }),

        ...(notes.trim() && {
            notes: notes.trim(),
        }),
        };

        return createWalkinVisit(
        payload
        );
    },
 
 
    onSuccess: (visit) => {
 
      navigate(
        `/visits/${visit.id}`
      );
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
 
        setFormError(
          data?.message
          ??
          data?.error
          ??
          "Unable to create walk-in visit."
        );
 
        return;
      }
 
      setFormError(
        "Unable to create walk-in visit."
      );
    },
  });
 
 
  function handleSubmit(
    event: FormEvent
  ) {
 
    event.preventDefault();
 
    setFormError(null);
 
 
    if (
      !hostId
      ||
      !siteId
      ||
      !destinationId
    ) {
 
      setFormError(
        "Host, site and destination are required."
      );
 
      return;
    }
 
 
    if (
      visitorMode === "existing"
      &&
      !visitorId
    ) {
 
      setFormError(
        "Please select a visitor."
      );
 
      return;
    }
 
 
    if (
      visitorMode === "new"
      &&
      (
        !firstName.trim()
        ||
        !lastName.trim()
        ||
        !phone.trim()
      )
    ) {
 
      setFormError(
        "First name, last name and phone number are required."
      );
 
      return;
    }
 
 
    createMutation.mutate();
  }
 
 
  const loading =
    visitorsQuery.isLoading
    ||
    hostsQuery.isLoading
    ||
    sitesQuery.isLoading
    ||
    destinationsQuery.isLoading;
 
 
  if (loading) {
    return <div>Loading form...</div>;
  }
 
 
  if (
    visitorsQuery.isError
    ||
    hostsQuery.isError
    ||
    sitesQuery.isError
    ||
    destinationsQuery.isError
  ) {
 
    return (
      <div className="page-error">
        Unable to load walk-in form data.
      </div>
    );
  }
 
 
  const visitors =
    visitorsQuery.data ?? [];
 
  const hosts =
    hostsQuery.data ?? [];
 
  const sites =
    sitesQuery.data ?? [];
 
  const destinations =
    destinationsQuery.data ?? [];
 
 
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
            Walk-in Visit
          </h1>
 
          <p>
            Register a visitor who has
            arrived without a prebooking.
          </p>
 
        </div>
 
      </div>
 
 
      <form
        className="visit-form"
        onSubmit={handleSubmit}
      >
 
        {formError && (
          <div className="form-error">
            {formError}
          </div>
        )}
 
 
        <section className="form-card">
 
          <h2>
            Visitor
          </h2>
 
 
          <div className="visitor-mode">
 
            <label className="radio-option">
 
              <input
                type="radio"
                checked={
                  visitorMode === "new"
                }
                onChange={() =>
                  setVisitorMode("new")
                }
              />
 
              New Visitor
 
            </label>
 
 
            <label className="radio-option">
 
              <input
                type="radio"
                checked={
                  visitorMode ===
                  "existing"
                }
                onChange={() =>
                  setVisitorMode(
                    "existing"
                  )
                }
              />
 
              Existing Visitor
 
            </label>
 
          </div>
 
 
          {visitorMode ===
          "existing" ? (
 
            <div className="form-field">
 
              <label>
                Visitor *
              </label>
 
              <select
                value={visitorId}
                onChange={(event) =>
                  setVisitorId(
                    event.target.value
                  )
                }
              >
 
                <option value="">
                  Select visitor
                </option>
 
                {visitors.map(
                  (visitor) => (
 
                    <option
                      key={visitor.id}
                      value={visitor.id}
                    >
                      {[
                        visitor.first_name,
                        visitor.middle_name,
                        visitor.last_name,
                      ]
                        .filter(Boolean)
                        .join(" ")}
                    </option>
 
                  )
                )}
 
              </select>
 
            </div>
 
          ) : (
 
            <>
              <div className="form-grid">
 
                <FormInput
                  label="First Name *"
                  value={firstName}
                  onChange={setFirstName}
                />
 
                <FormInput
                  label="Last Name *"
                  value={lastName}
                  onChange={setLastName}
                />
 
                <FormInput
                  label="Email"
                  type="email"
                  value={email}
                  onChange={setEmail}
                />
 
                <FormInput
                  label="Phone *"
                  value={phone}
                  onChange={setPhone}
                />
 
                <FormInput
                  label="Company"
                  value={company}
                  onChange={setCompany}
                />
 
                <FormInput
                  label="Nationality"
                  value={nationality}
                  onChange={setNationality}
                />
 
                <FormInput
                  label="ID Number"
                  value={idNumber}
                  onChange={setIdNumber}
                />
 
                <FormInput
                  label="Passport Number"
                  value={passportNumber}
                  onChange={
                    setPassportNumber
                  }
                />
 
                <FormInput
                  label={
                    "Vehicle Registration"
                  }
                  value={
                    vehicleRegistration
                  }
                  onChange={
                    setVehicleRegistration
                  }
                />
 
              </div>
 
              <p className="form-help">
                Capture identification
                information when available.
              </p>
            </>
 
          )}
 
        </section>
 
 
        <section className="form-card">
 
          <h2>
            Host & Location
          </h2>
 
          <div className="form-grid">
 
            <div className="form-field">
 
              <label>
                Host *
              </label>
 
              <select
                value={hostId}
                onChange={(event) =>
                  setHostId(
                    event.target.value
                  )
                }
              >
 
                <option value="">
                  Select host
                </option>
 
                {hosts.map((host) => (
 
                  <option
                    key={host.id}
                    value={host.id}
                  >
                    {[
                      host.first_name,
                      host.last_name,
                    ]
                      .filter(Boolean)
                      .join(" ")}
                  </option>
 
                ))}
 
              </select>
 
            </div>
 
 
            <div className="form-field">
 
              <label>
                Site *
              </label>
 
              <select
                value={siteId}
                onChange={(event) =>
                  setSiteId(
                    event.target.value
                  )
                }
              >
 
                <option value="">
                  Select site
                </option>
 
                {sites.map((site) => (
 
                  <option
                    key={site.id}
                    value={site.id}
                  >
                    {site.name}
                  </option>
 
                ))}
 
              </select>
 
            </div>
 
 
            <div className="form-field">
 
              <label>
                Destination *
              </label>
 
              <select
                value={destinationId}
                onChange={(event) =>
                  setDestinationId(
                    event.target.value
                  )
                }
              >
 
                <option value="">
                  Select destination
                </option>
 
                {destinations.map(
                  (destination) => (
 
                    <option
                      key={
                        destination.id
                      }
                      value={
                        destination.id
                      }
                    >
                      {
                        destination.name
                      }
                    </option>
 
                  )
                )}
 
              </select>
 
            </div>
 
          </div>
 
        </section>
 
 
        <section className="form-card">
 
          <h2>
            Visit Details
          </h2>
 
          <div className="form-field">
 
            <label>
              Purpose
            </label>
 
            <textarea
              rows={3}
              value={purpose}
              onChange={(event) =>
                setPurpose(
                  event.target.value
                )
              }
            />
 
          </div>
 
 
          <div className="form-field">
 
            <label>
              Notes
            </label>
 
            <textarea
              rows={3}
              value={notes}
              onChange={(event) =>
                setNotes(
                  event.target.value
                )
              }
            />
 
          </div>
 
        </section>
 
 
        <div className="form-actions">
 
          <Link
            to="/visits"
            className={
              "button button-secondary"
            }
          >
            Cancel
          </Link>
 
          <button
            type="submit"
            className="button"
            disabled={
              createMutation.isPending
            }
          >
            {
              createMutation.isPending
                ? "Registering..."
                : "Register Walk-in"
            }
          </button>
 
        </div>
 
      </form>
 
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