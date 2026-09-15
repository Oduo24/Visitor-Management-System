import {
  useState,
} from "react";
 
import {
  Link,
} from "react-router-dom";
 
import {
  useQuery,
} from "@tanstack/react-query";
 
import {
  getSites,
} from "../../api/sites.api";
 
import {
  getVisitActivityReport,
  type VisitActivityFilters,
} from "../../api/reports.api";
 
 
export function VisitActivityReportPage() {
 
  const [
    filters,
    setFilters,
  ] = useState<VisitActivityFilters>({
    site_id: "",
    status: "",
    visit_type: "",
    start_date: "",
    end_date: "",
  });
 
 
  const sitesQuery =
    useQuery({
      queryKey: ["sites"],
      queryFn: getSites,
    });
 
 
  const reportQuery =
    useQuery({
 
      queryKey: [
        "visit-activity-report",
        filters,
      ],
 
      queryFn: () =>
        getVisitActivityReport(
          filters
        ),
 
    });
 
 
  const sites =
    sitesQuery.data ?? [];
 
  const visits =
    reportQuery.data ?? [];
 
 
  function setFilter<
    K extends keyof VisitActivityFilters
  >(
    field: K,
    value: VisitActivityFilters[K]
  ) {
 
    setFilters(
      (current) => ({
        ...current,
        [field]: value,
      })
    );
  }
 
 
  function clearFilters() {
 
    setFilters({
      site_id: "",
      status: "",
      visit_type: "",
      start_date: "",
      end_date: "",
    });
  }
 
 
  return (
    <div className="page">
 
      <div className="page-heading">
 
        <div>
 
          <h1>
            Visit Activity Report
          </h1>
 
          <p>
            Review visit activity by
            site, status, type and date.
          </p>
 
        </div>
 
      </div>
 
 
      <section className="detail-card">
 
        <div className="section-heading">
 
          <h2>
            Filters
          </h2>
 
          <button
            type="button"
            onClick={
              clearFilters
            }
          >
            Clear Filters
          </button>
 
        </div>
 
 
        <div className="form-grid">
 
          <div className="form-field">
 
            <label>
              Site
            </label>
 
            <select
              value={
                filters.site_id
                ?? ""
              }
              onChange={(event) =>
                setFilter(
                  "site_id",
                  event.target.value
                )
              }
            >
 
              <option value="">
                All Sites
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
 
            <label>
              Status
            </label>
 
            <select
              value={
                filters.status
                ?? ""
              }
              onChange={(event) =>
                setFilter(
                  "status",
                  event.target.value
                )
              }
            >
 
              <option value="">
                All Statuses
              </option>
 
              <option value="PENDING">
                Pending
              </option>
 
              <option value="APPROVED">
                Approved
              </option>
 
              <option value="REJECTED">
                Rejected
              </option>
 
              <option value="CHECKED_IN">
                Checked In
              </option>
 
              <option value="CHECKED_OUT">
                Checked Out
              </option>
 
            </select>
 
          </div>
 
 
          <div className="form-field">
 
            <label>
              Visit Type
            </label>
 
            <select
              value={
                filters.visit_type
                ?? ""
              }
              onChange={(event) =>
                setFilter(
                  "visit_type",
                  event.target.value
                )
              }
            >
 
              <option value="">
                All Types
              </option>
 
              <option value="PREBOOK">
                Prebook
              </option>
 
              <option value="WALK_IN">
                Walk-in
              </option>
 
            </select>
 
          </div>
 
 
          <div className="form-field">
 
            <label>
              From
            </label>
 
            <input
              type="date"
              value={
                filters.start_date
                ?? ""
              }
              onChange={(event) =>
                setFilter(
                  "start_date",
                  event.target.value
                )
              }
            />
 
          </div>
 
 
          <div className="form-field">
 
            <label>
              To
            </label>
 
            <input
              type="date"
              value={
                filters.end_date
                ?? ""
              }
              onChange={(event) =>
                setFilter(
                  "end_date",
                  event.target.value
                )
              }
            />
 
          </div>
 
        </div>
 
      </section>
 
 
      <div className="report-summary">
 
        <strong>
          {visits.length}
        </strong>
 
        {" "}
        visit{
          visits.length === 1
            ? ""
            : "s"
        } found
 
      </div>
 
 
      {reportQuery.isLoading ? (
 
        <div>
          Loading report...
        </div>
 
      ) : reportQuery.isError ? (
 
        <div className="form-error">
          Unable to load report.
        </div>
 
      ) : (
 
        <div className="table-wrapper">
 
          <table>
 
            <thead>
 
              <tr>
                <th>Visitor</th>
                <th>Host</th>
                <th>Site</th>
                <th>Type</th>
                <th>Status</th>
                <th>Expected Arrival</th>
                <th>Check In</th>
                <th>Check Out</th>
                <th></th>
              </tr>
 
            </thead>
 
 
            <tbody>
 
              {visits.map(
                (visit) => (
 
                  <tr key={visit.id}>
 
                    <td>
                      {visit.visitor_name}
                    </td>
 
                    <td>
                      {visit.host_name}
                    </td>
 
                    <td>
                      {visit.site_name}
                    </td>
 
                    <td>
                      {formatLabel(
                        visit.visit_type
                      )}
                    </td>
 
                    <td>
                      {formatLabel(
                        visit.status
                      )}
                    </td>
 
                    <td>
                      {formatDateTime(
                        visit.expected_arrival
                      )}
                    </td>
 
                    <td>
                      {formatDateTime(
                        visit.checked_in_at
                      )}
                    </td>
 
                    <td>
                      {formatDateTime(
                        visit.checked_out_at
                      )}
                    </td>
 
                    <td>
 
                      <Link
                        to={
                          `/visits/${visit.id}`
                        }
                      >
                        View
                      </Link>
 
                    </td>
 
                  </tr>
 
                )
              )}
 
            </tbody>
 
          </table>
 
 
          {visits.length === 0 && (
 
            <div className="empty-state">
              No visits match the selected filters.
            </div>
 
          )}
 
        </div>
 
      )}
 
    </div>
  );
}
 
 
function formatLabel(
  value: string
) {
 
  return value
    .replaceAll(
      "_",
      " "
    )
    .toLowerCase()
    .replace(
      /\b\w/g,
      (letter) =>
        letter.toUpperCase()
    );
}
 
 
function formatDateTime(
  value:
    | string
    | null
    | undefined
) {
 
  if (!value) {
    return "-";
  }
 
  return new Date(
    value
  ).toLocaleString();
}