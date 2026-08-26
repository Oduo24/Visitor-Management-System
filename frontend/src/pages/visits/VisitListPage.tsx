import {
  useQuery,
  useMutation,
} from "@tanstack/react-query";
 
import {
  Link,
  useNavigate,
} from "react-router-dom";
 
import {
  getVisits,
  getVisitByCode,
} from "../../api/visits.api";
 
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
 
 
export function VisitListPage() {
 
  const {
    data: visits = [],
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ["visits"],
    queryFn: getVisits,
  });

  const navigate =
    useNavigate();
  
  const [
    visitorCode,
    setVisitorCode,
  ] = useState("");
  
  const [
    lookupError,
    setLookupError,
  ] = useState<string | null>(
    null
  );
 

  const visitorCodeMutation =
  useMutation({
 
    mutationFn: (
      code: string
    ) => {
      return getVisitByCode(
        code
      );
    },
 
    onSuccess: (visit) => {
 
      setLookupError(null);
 
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
 
        setLookupError(
          data?.message
          ??
          data?.error
          ??
          "No visit was found for that visitor code."
        );
 
        return;
      }
 
      setLookupError(
        "No visit was found for that visitor code."
      );
    },
 
  });

 
  if (isLoading) {
    return (
      <div>
        Loading visits...
      </div>
    );
  }


  function handleVisitorCodeLookup() {
 
    setLookupError(null);
  
    const code =
      visitorCode.trim();
  
  
    if (!code) {
  
      setLookupError(
        "Enter a visitor code."
      );
  
      return;
    }
  
  
    if (
      !/^\d{6}$/.test(code)
    ) {
  
      setLookupError(
        "Visitor code must be 6 digits."
      );
  
      return;
    }
  
  
    // Fast path:
    // use data already loaded in the browser.
    const cachedVisit =
      visits?.find(
        (visit) =>
          visit.visitor_code
          === code
      );
  
  
    if (cachedVisit) {
  
      navigate(
        `/visits/${cachedVisit.id}`
      );
  
      return;
    }
  
  
    // Authoritative fallback:
    // the visit may not be in the
    // currently loaded list.
    visitorCodeMutation.mutate(
      code
    );
  }
 
 
  if (isError) {
 
    return (
      <div className="page-error">
 
        Unable to load visits.
 
        <div>
          {
            error instanceof Error
              ? error.message
              : ""
          }
        </div>
 
      </div>
    );
  }
 
 
  return (
    <div>
 
      <div className="page-heading">
 
        <div>
          <h1>
            Visits
          </h1>
 
          <p>
            Manage visitor appointments
            and arrivals.
          </p>
        </div>
 
        <div className="page-actions">
 
          <Link
            to="/visits/prebook"
            className="button"
          >
            Prebook Visit
          </Link>
 
          <Link
            to="/visits/walk-in"
            className="button button-secondary"
          >
            Walk-in
          </Link>
 
        </div>
 
      </div>

      <section className="visitor-code-lookup">
 
        <div>
      
          <h2>
            Reception Lookup
          </h2>
      
          <p className="form-help">
            Enter the visitor's 6-digit
            code to locate their visit.
          </p>
      
        </div>
      
      
        <div className="visitor-code-lookup-form">
      
          <input
            type="text"
            inputMode="numeric"
            maxLength={6}
            placeholder="Visitor code"
            value={visitorCode}
            onChange={(event) => {
      
              const value =
                event.target.value
                  .replace(
                    /\D/g,
                    ""
                  )
                  .slice(
                    0,
                    6
                  );
      
              setVisitorCode(
                value
              );
      
              setLookupError(
                null
              );
            }}
            onKeyDown={(event) => {
      
              if (
                event.key === "Enter"
              ) {
                handleVisitorCodeLookup();
              }
            }}
          />
      
      
          <button
            type="button"
            className="button"
            disabled={
              visitorCodeMutation.isPending
            }
            onClick={
              handleVisitorCodeLookup
            }
          >
            {
              visitorCodeMutation.isPending
                ? "Searching..."
                : "Find Visit"
            }
          </button>
      
        </div>
      
      
        {lookupError && (
      
          <div className="form-error">
            {lookupError}
          </div>
      
        )}
      
      </section>
 
 
      <div className="table-card">
 
        {visits.length === 0 ? (
 
          <div className="empty-state">
            No visits found.
          </div>
 
        ) : (
 
          <table className="data-table">

            <thead>
              <tr>
                <th>Visitor</th>
                <th>Host</th>
                <th>Site</th>
                <th>Destination</th>
                <th>Status</th>
                <th>Type</th>
                <th>Purpose</th>
                <th>Expected Arrival</th>
                <th>Visitor Code</th>
                <th></th>
              </tr>
            </thead>

            <tbody>

              {visits.map((visit) => (

                <tr key={visit.id}>

                  <td>
                    {visit.visitor_name ?? "-"}
                  </td>

                  <td>
                    {visit.host_name ?? "-"}
                  </td>

                  <td>
                    {visit.site_name ?? "-"}
                  </td>

                  <td>
                    {visit.destination_name ?? "-"}
                  </td>

                  <td>
                    <StatusBadge
                      status={visit.status}
                    />
                  </td>

                  <td>
                    {visit.visit_type.replaceAll(
                      "_",
                      " "
                    )}
                  </td>

                  <td>
                    {visit.purpose ?? "-"}
                  </td>

                  <td>
                    {formatDate(
                      visit.expected_arrival
                    )}
                  </td>

                  <td>
                    {visit.visitor_code ?? "-"}
                  </td>

                  <td>
                    <Link
                      to={`/visits/${visit.id}`}
                    >
                      View
                    </Link>
                  </td>

                </tr>

              ))}

            </tbody>

          </table>
 
        )}
 
      </div>
 
    </div>
  );
}


