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
  createPrebookVisit,
} from "../../api/visits.api";
 
import {
  getVisitors,
  getHosts,
  getSites,
  getDestinations,
} from "../../api/lookups.api";

import { createVisitor } from "../../api/visitors.api";
 
type VisitorMode =
  | "existing"
  | "new";

export function PrebookVisitPage() {
 
  const navigate = useNavigate();
 
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
    expectedArrival,
    setExpectedArrival,
  ] = useState("");
 
  const [
    expectedDeparture,
    setExpectedDeparture,
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

  const [
  visitorMode,
  setVisitorMode,
] = useState<VisitorMode>(
  "existing"
);
 
const [
  newVisitorFirstName,
  setNewVisitorFirstName,
] = useState("");
 
const [
  newVisitorLastName,
  setNewVisitorLastName,
] = useState("");
 
const [
  newVisitorEmail,
  setNewVisitorEmail,
] = useState("");
 
const [
  newVisitorPhone,
  setNewVisitorPhone,
] = useState("");
 
const [
  newVisitorCompany,
  setNewVisitorCompany,
] = useState("");
 
 
  const createMutation = useMutation({
 
  mutationFn: async () => {
 
    let resolvedVisitorId =
      visitorId;
 
    /*
     * New visitor:
     * create Visitor first.
     */
    if (
      visitorMode === "new"
    ) {
 
      const visitor =
        await createVisitor({
          first_name:
            newVisitorFirstName.trim(),
 
          last_name:
            newVisitorLastName.trim(),
 
          email:
            newVisitorEmail.trim()
              || null,
 
          phone:
            newVisitorPhone.trim(),
 
          company:
            newVisitorCompany.trim()
              || null,
        });
 
      resolvedVisitorId =
        visitor.id;
    }
 
 
    /*
     * Create the actual
     * prebooked Visit.
     */
    return createPrebookVisit({
      visitor_id:
        resolvedVisitorId,
 
      host_id:
        hostId,
 
      site_id:
        siteId,
 
      destination_id:
        destinationId,
 
      expected_arrival:
        new Date(
          expectedArrival
        ).toISOString(),
 
      expected_departure:
        expectedDeparture
          ? new Date(
              expectedDeparture
            ).toISOString()
          : null,
 
      purpose:
        purpose.trim()
          || null,
 
      notes:
        notes.trim()
          || null,
    });
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
        "Unable to create prebooked visit."
      );
 
      return;
    }
 
    setFormError(
      "Unable to create prebooked visit."
    );
  },
});
 
 
  const loadingLookups =
    visitorsQuery.isLoading
    ||
    hostsQuery.isLoading
    ||
    sitesQuery.isLoading
    ||
    destinationsQuery.isLoading;
 
 
  const lookupError =
    visitorsQuery.isError
    ||
    hostsQuery.isError
    ||
    sitesQuery.isError
    ||
    destinationsQuery.isError;
 
 
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
    ||
    !expectedArrival
  ) {
 
    setFormError(
      "Please complete all required visit fields."
    );
 
    return;
  }
 
 
  /*
   * Existing visitor
   */
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
 
 
  /*
   * New visitor
   */
  if (
    visitorMode === "new"
  ) {
 
    if (
      !newVisitorFirstName.trim()
      ||
      !newVisitorLastName.trim()
    ) {
 
      setFormError(
        "First name and last name are required."
      );
 
      return;
    }
 
 
    if (
      !newVisitorPhone.trim()
    ) {
 
      setFormError(
        "Phone number is required"
      );
 
      return;
    }
  }
 
 
  if (
    expectedDeparture
    &&
    new Date(
      expectedDeparture
    ) <=
    new Date(
      expectedArrival
    )
  ) {
 
    setFormError(
      "Expected departure must be after expected arrival."
    );
 
    return;
  }
 
 
  createMutation.mutate();
}
 
 
  if (loadingLookups) {
    return (
      <div>
        Loading form data...
      </div>
    );
  }
 
 
  if (lookupError) {
    return (
      <div className="page-error">
        Unable to load the data required
        to create a visit.
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
            Prebook Visit
          </h1>
 
          <p>
            Schedule a visitor before
            their arrival.
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
                Visitor & Host
            </h2>
            
            
            <div className="visitor-mode">
            
                <label className="radio-option">
            
                <input
                    type="radio"
                    name="visitorMode"
                    value="existing"
                    checked={
                    visitorMode
                    ===
                    "existing"
                    }
                    onChange={() => {
                    setVisitorMode(
                        "existing"
                    );
            
                    setFormError(
                        null
                    );
                    }}
                />
            
                Existing Visitor
            
                </label>
            
            
                <label className="radio-option">
            
                <input
                    type="radio"
                    name="visitorMode"
                    value="new"
                    checked={
                    visitorMode
                    ===
                    "new"
                    }
                    onChange={() => {
                    setVisitorMode(
                        "new"
                    );
            
                    setFormError(
                        null
                    );
                    }}
                />
            
                New Visitor
            
                </label>
            
            </div>
            
            
            {visitorMode ===
            "existing" ? (
            
                <div className="form-field">
            
                <label htmlFor="visitor">
                    Visitor *
                </label>
            
                <select
                    id="visitor"
                    value={visitorId}
                    onChange={(event) =>
                    setVisitorId(
                        event.target.value
                    )
                    }
                    required
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
                        {
                            [
                            visitor.first_name,
                            visitor.middle_name,
                            visitor.last_name,
                            ]
                            .filter(Boolean)
                            .join(" ")
                        }
            
                        {
                            visitor.email
                            ? ` — ${visitor.email}`
                            : ""
                        }
            
                        </option>
            
                    )
                    )}
            
                </select>
            
                </div>
            
            ) : (
            
                <div className="new-visitor-panel">
            
                <div className="form-grid">
            
                    <div className="form-field">
            
                    <label
                        htmlFor="newVisitorFirstName"
                    >
                        First Name *
                    </label>
            
                    <input
                        id="newVisitorFirstName"
                        type="text"
                        value={
                        newVisitorFirstName
                        }
                        onChange={(event) =>
                        setNewVisitorFirstName(
                            event.target.value
                        )
                        }
                    />
            
                    </div>
            
            
                    <div className="form-field">
            
                    <label
                        htmlFor="newVisitorLastName"
                    >
                        Last Name *
                    </label>
            
                    <input
                        id="newVisitorLastName"
                        type="text"
                        value={
                        newVisitorLastName
                        }
                        onChange={(event) =>
                        setNewVisitorLastName(
                            event.target.value
                        )
                        }
                    />
            
                    </div>
            
            
                    <div className="form-field">
            
                    <label
                        htmlFor="newVisitorEmail"
                    >
                        Email
                    </label>
            
                    <input
                        id="newVisitorEmail"
                        type="email"
                        value={
                        newVisitorEmail
                        }
                        onChange={(event) =>
                        setNewVisitorEmail(
                            event.target.value
                        )
                        }
                    />
            
                    </div>
            
            
                    <div className="form-field">
            
                    <label
                        htmlFor="newVisitorPhone"
                    >
                        Phone
                    </label>
            
                    <input
                        id="newVisitorPhone"
                        type="tel"
                        value={
                        newVisitorPhone
                        }
                        onChange={(event) =>
                        setNewVisitorPhone(
                            event.target.value
                        )
                        }
                    />
            
                    </div>
            
            
                    <div className="form-field">
            
                    <label
                        htmlFor="newVisitorCompany"
                    >
                        Company
                    </label>
            
                    <input
                        id="newVisitorCompany"
                        type="text"
                        value={
                        newVisitorCompany
                        }
                        onChange={(event) =>
                        setNewVisitorCompany(
                            event.target.value
                        )
                        }
                    />
            
                    </div>
            
                </div>
            
            
                <p className="form-help">
                    Provide at least an email
                    address or phone number.
                    Additional visitor details can
                    be completed later.
                </p>
            
                </div>
            
            )}
            
            
            <div className="form-field">
            
                <label htmlFor="host">
                Host *
                </label>
            
                <select
                id="host"
                value={hostId}
                onChange={(event) =>
                    setHostId(
                    event.target.value
                    )
                }
                required
                >
            
                <option value="">
                    Select host
                </option>
            
                {hosts.map(
                    (host) => (
            
                    <option
                        key={host.id}
                        value={host.id}
                    >
                        {
                        [
                            host.first_name,
                            host.last_name,
                        ]
                            .filter(Boolean)
                            .join(" ")
                        }
                    </option>
            
                    )
                )}
            
                </select>
            
            </div>
            
            </section>
 
 
        <section className="form-card">
 
          <h2>
            Location
          </h2>
 
          <div className="form-grid">
 
            <div className="form-field">
 
              <label htmlFor="site">
                Site *
              </label>
 
              <select
                id="site"
                value={siteId}
                onChange={(event) =>
                  setSiteId(
                    event.target.value
                  )
                }
                required
              >
 
                <option value="">
                  Select site
                </option>
 
                {sites.map(
                  (site) => (
 
                    <option
                      key={site.id}
                      value={site.id}
                    >
                      {site.name}
                    </option>
 
                  )
                )}
 
              </select>
 
            </div>
 
 
            <div className="form-field">
 
              <label htmlFor="destination">
                Destination *
              </label>
 
              <select
                id="destination"
                value={destinationId}
                onChange={(event) =>
                  setDestinationId(
                    event.target.value
                  )
                }
                required
              >
 
                <option value="">
                  Select destination
                </option>
 
                {destinations.map(
                  (destination) => (
 
                    <option
                      key={destination.id}
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
            Schedule
          </h2>
 
          <div className="form-grid">
 
            <div className="form-field">
 
              <label htmlFor="arrival">
                Expected Arrival *
              </label>
 
              <input
                id="arrival"
                type="datetime-local"
                value={
                  expectedArrival
                }
                onChange={(event) =>
                  setExpectedArrival(
                    event.target.value
                  )
                }
                required
              />
 
            </div>
 
 
            <div className="form-field">
 
              <label htmlFor="departure">
                Expected Departure
              </label>
 
              <input
                id="departure"
                type="datetime-local"
                value={
                  expectedDeparture
                }
                onChange={(event) =>
                  setExpectedDeparture(
                    event.target.value
                  )
                }
              />
 
            </div>
 
          </div>
 
        </section>
 
 
        <section className="form-card">
 
          <h2>
            Visit Details
          </h2>
 
          <div className="form-field">
 
            <label htmlFor="purpose">
              Purpose
            </label>
 
            <textarea
              id="purpose"
              value={purpose}
              onChange={(event) =>
                setPurpose(
                  event.target.value
                )
              }
              rows={3}
              placeholder={
                "Reason for the visit"
              }
            />
 
          </div>
 
 
          <div className="form-field">
 
            <label htmlFor="notes">
              Notes
            </label>
 
            <textarea
              id="notes"
              value={notes}
              onChange={(event) =>
                setNotes(
                  event.target.value
                )
              }
              rows={3}
            />
 
          </div>
 
        </section>
 
 
        <div className="form-actions">
 
          <Link
            to="/visits"
            className="button button-secondary"
          >
            Cancel
          </Link>
 
          <button
            className="button"
            type="submit"
            disabled={
              createMutation.isPending
            }
          >
            {
              createMutation.isPending
                ? "Creating Prebook..."
                : "Create Prebook"
            }
          </button>
 
        </div>
 
      </form>
 
    </div>
  );
}