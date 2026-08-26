import {
  useQuery,
} from "@tanstack/react-query";
 
import {
  Link,
} from "react-router-dom";
 
import {
  getVisits,
} from "../../api/visits.api";
 
import {
  StatusBadge,
} from "../../components/common/StatusBadge";
 
 
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
 
 
  if (isLoading) {
    return (
      <div>
        Loading visits...
      </div>
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