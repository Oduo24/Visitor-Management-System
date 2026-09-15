import {
  useMemo,
  useState,
  type FormEvent,
} from "react";
 
import axios from "axios";
 
import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
 
import {
  createSite,
  deleteSite,
  getSites,
  updateSite,
} from "../../api/sites.api";
 
import {
  getOrganizations,
} from "../../api/organizations.api";
 
import type {
  CreateSitePayload,
  Site,
} from "../../types/site";
 
 
const EMPTY_FORM: CreateSitePayload = {
  organization_id: "",
 
  name: "",
  code: "",
 
  address: null,
  city: null,
  country: null,
 
  timezone: "Africa/Nairobi",
 
  phone: null,
  email: null,
 
  is_active: true,
};
 
 
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
 
 
export function SiteListPage() {
 
  const queryClient =
    useQueryClient();
 
  const [
    search,
    setSearch,
  ] = useState("");
 
  const [
    showForm,
    setShowForm,
  ] = useState(false);
 
  const [
    editingSite,
    setEditingSite,
  ] = useState<Site | null>(
    null
  );
 
  const [
    form,
    setForm,
  ] = useState<CreateSitePayload>({
    ...EMPTY_FORM,
  });
 
  const [
    formError,
    setFormError,
  ] = useState<string | null>(
    null
  );
 
 
  const sitesQuery =
    useQuery({
 
      queryKey: [
        "sites",
      ],
 
      queryFn:
        getSites,
 
    });
 
 
  const organizationsQuery =
    useQuery({
 
      queryKey: [
        "organizations",
      ],
 
      queryFn:
        getOrganizations,
 
    });
 
 
  const saveMutation =
    useMutation({
 
      mutationFn: () => {
 
        if (editingSite) {
 
          return updateSite(
            editingSite.id,
            form
          );
        }
 
        return createSite(
          form
        );
      },
 
 
      onSuccess: async () => {
 
        setFormError(null);
 
        closeForm();
 
        await queryClient
          .invalidateQueries({
            queryKey: [
              "sites",
            ],
          });
      },
 
 
      onError: (error) => {
 
        setFormError(
          getErrorMessage(
            error,
            "Unable to save site."
          )
        );
      },
 
    });
 
 
  const deleteMutation =
    useMutation({
 
      mutationFn:
        deleteSite,
 
 
      onSuccess: async () => {
 
        await queryClient
          .invalidateQueries({
            queryKey: [
              "sites",
            ],
          });
      },
 
 
      onError: (error) => {
 
        window.alert(
          getErrorMessage(
            error,
            "Unable to delete site."
          )
        );
      },
 
    });
 
 
  const sites =
    sitesQuery.data ?? [];
 
  const organizations =
    organizationsQuery.data ?? [];
 
 
  const organizationMap =
  useMemo<Map<string, string>>(
    () => {
 
      const map =
        new Map<string, string>();
 
      organizations.forEach(
        (organization) => {
 
          map.set(
            organization.id,
            organization.name
          );
        }
      );
 
      return map;
    },
    [
      organizations,
    ]
  );
 
 
  const filteredSites =
    useMemo(() => {
 
      const term =
        search
          .trim()
          .toLowerCase();
 
      if (!term) {
        return sites;
      }
 
      return sites.filter(
        (site) => {
 
          const searchable = [
            site.name,
            site.code,
            site.address,
            site.city,
            site.country,
            site.timezone,
            site.phone,
            site.email,
            organizationMap.get(
              site.organization_id
            ),
          ]
            .filter(Boolean)
            .join(" ")
            .toLowerCase();
 
          return searchable.includes(
            term
          );
        }
      );
 
    }, [
      sites,
      search,
      organizationMap,
    ]);
 
 
  function setField<
    K extends keyof CreateSitePayload
  >(
    field: K,
    value: CreateSitePayload[K]
  ) {
 
    setForm(
      (current) => ({
        ...current,
        [field]: value,
      })
    );
  }
 
 
  function openCreateForm() {
 
    setEditingSite(
      null
    );
 
    setForm({
      ...EMPTY_FORM,
 
      organization_id:
        organizations.length === 1
          ? organizations[0].id
          : "",
    });
 
    setFormError(null);
 
    setShowForm(true);
  }
 
 
  function openEditForm(
    site: Site
  ) {
 
    setEditingSite(
      site
    );
 
    setForm({
      organization_id:
        site.organization_id,
 
      name:
        site.name,
 
      code:
        site.code,
 
      address:
        site.address,
 
      city:
        site.city,
 
      country:
        site.country,
 
      timezone:
        site.timezone,
 
      phone:
        site.phone,
 
      email:
        site.email,
 
      is_active:
        site.is_active,
    });
 
    setFormError(null);
 
    setShowForm(true);
  }
 
 
  function closeForm() {
 
    setShowForm(false);
 
    setEditingSite(
      null
    );
 
    setForm({
      ...EMPTY_FORM,
    });
 
    setFormError(null);
  }
 
 
  function handleSubmit(
    event: FormEvent
  ) {
 
    event.preventDefault();
 
    setFormError(null);
 
 
    if (
      !form.organization_id
    ) {
 
      setFormError(
        "Organization is required."
      );
 
      return;
    }
 
 
    if (
      !form.name.trim()
    ) {
 
      setFormError(
        "Site name is required."
      );
 
      return;
    }
 
 
    if (
      form.name.trim().length < 2
    ) {
 
      setFormError(
        "Site name must contain at least 2 characters."
      );
 
      return;
    }
 
 
    if (
      !form.code.trim()
    ) {
 
      setFormError(
        "Site code is required."
      );
 
      return;
    }
 
 
    if (
      form.code.trim().length < 2
      ||
      form.code.trim().length > 20
    ) {
 
      setFormError(
        "Site code must contain between 2 and 20 characters."
      );
 
      return;
    }
 
 
    if (
      !form.timezone?.trim()
    ) {
 
      setFormError(
        "Timezone is required."
      );
 
      return;
    }
 
 
    saveMutation.mutate();
  }
 
 
  if (
    sitesQuery.isLoading
    ||
    organizationsQuery.isLoading
  ) {
 
    return (
      <div>
        Loading sites...
      </div>
    );
  }
 
 
  if (
    sitesQuery.isError
    ||
    organizationsQuery.isError
  ) {
 
    return (
      <div className="form-error">
        Unable to load site administration data.
      </div>
    );
  }
 
 
  return (
    <div className="page">
 
      <div className="page-heading">
 
        <div>
 
          <h1>
            Sites
          </h1>
 
          <p>
            Manage physical locations
            where visitors are received.
          </p>
 
        </div>
 
 
        <button
          type="button"
          className="button"
          onClick={
            openCreateForm
          }
        >
          Add Site
        </button>
 
      </div>
 
 
      <div className="list-toolbar">
 
        <input
          type="search"
          placeholder="Search sites..."
          value={search}
          onChange={(event) =>
            setSearch(
              event.target.value
            )
          }
        />
 
      </div>
 
 
      {showForm && (
 
        <section className="detail-card site-form-card">
 
          <div className="section-heading">
 
            <h2>
              {
                editingSite
                  ? "Edit Site"
                  : "Add Site"
              }
            </h2>
 
 
            <button
              type="button"
              onClick={
                closeForm
              }
            >
              Cancel
            </button>
 
          </div>
 
 
          <form
            onSubmit={
              handleSubmit
            }
          >
 
            <div className="form-grid">
 
              <div className="form-field">
 
                <label>
                  Organization *
                </label>
 
                <select
                  value={
                    form.organization_id
                  }
                  onChange={(event) =>
                    setField(
                      "organization_id",
                      event.target.value
                    )
                  }
                >
 
                  <option value="">
                    Select organization
                  </option>
 
 
                  {organizations
                    .filter(
                      (organization) =>
                        organization.is_active
                        ||
                        organization.id
                        ===
                        form.organization_id
                    )
                    .map(
                      (organization) => (
 
                        <option
                          key={
                            organization.id
                          }
                          value={
                            organization.id
                          }
                        >
                          {
                            organization.name
                          }
                          {" "}
                          (
                          {
                            organization.code
                          }
                          )
                        </option>
 
                      )
                    )}
 
                </select>
 
              </div>
 
 
              <SiteInput
                label="Site Name *"
                value={
                  form.name
                }
                onChange={(value) =>
                  setField(
                    "name",
                    value
                  )
                }
              />
 
 
              <SiteInput
                label="Site Code *"
                value={
                  form.code
                }
                onChange={(value) =>
                  setField(
                    "code",
                    value
                      .toUpperCase()
                  )
                }
              />
 
 
              <SiteInput
                label="Address"
                value={
                  form.address
                  ?? ""
                }
                onChange={(value) =>
                  setField(
                    "address",
                    value || null
                  )
                }
              />
 
 
              <SiteInput
                label="City"
                value={
                  form.city
                  ?? ""
                }
                onChange={(value) =>
                  setField(
                    "city",
                    value || null
                  )
                }
              />
 
 
              <SiteInput
                label="Country"
                value={
                  form.country
                  ?? ""
                }
                onChange={(value) =>
                  setField(
                    "country",
                    value || null
                  )
                }
              />
 
 
              <SiteInput
                label="Timezone *"
                value={
                  form.timezone
                  ?? ""
                }
                onChange={(value) =>
                  setField(
                    "timezone",
                    value
                  )
                }
              />
 
 
              <SiteInput
                label="Phone"
                type="tel"
                value={
                  form.phone
                  ?? ""
                }
                onChange={(value) =>
                  setField(
                    "phone",
                    value || null
                  )
                }
              />
 
 
              <SiteInput
                label="Email"
                type="email"
                value={
                  form.email
                  ?? ""
                }
                onChange={(value) =>
                  setField(
                    "email",
                    value || null
                  )
                }
              />
 
            </div>
 
 
            <label className="checkbox-field">
 
              <input
                type="checkbox"
                checked={
                  form.is_active
                  ?? true
                }
                onChange={(event) =>
                  setField(
                    "is_active",
                    event.target.checked
                  )
                }
              />
 
              Active site
 
            </label>
 
 
            {formError && (
 
              <div className="form-error">
                {formError}
              </div>
 
            )}
 
 
            <button
              type="submit"
              className="button"
              disabled={
                saveMutation.isPending
              }
            >
              {
                saveMutation.isPending
                  ? "Saving..."
                  : (
                    editingSite
                      ? "Save Changes"
                      : "Create Site"
                  )
              }
            </button>
 
          </form>
 
        </section>
 
      )}
 
 
      <div className="table-wrapper">
 
        <table>
 
          <thead>
 
            <tr>
              <th>Site</th>
              <th>Organization</th>
              <th>Location</th>
              <th>Contact</th>
              <th>Timezone</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
 
          </thead>
 
 
          <tbody>
 
            {filteredSites.map(
              (site) => (
 
                <tr key={site.id}>
 
                  <td>
 
                    <strong>
                      {site.name}
                    </strong>
 
                    <div className="table-secondary">
                      {site.code}
                    </div>
 
                  </td>
 
 
                  <td>
                    {
                      organizationMap.get(
                        site.organization_id
                      )
                      ??
                      "-"
                    }
                  </td>
 
 
                  <td>
 
                    {
                      [
                        site.city,
                        site.country,
                      ]
                        .filter(Boolean)
                        .join(", ")
                      ||
                      site.address
                      ||
                      "-"
                    }
 
                  </td>
 
 
                  <td>
 
                    <div>
                      {
                        site.phone
                        ?? "-"
                      }
                    </div>
 
                    <div className="table-secondary">
                      {
                        site.email
                        ?? "-"
                      }
                    </div>
 
                  </td>
 
 
                  <td>
                    {site.timezone}
                  </td>
 
 
                  <td>
 
                    <span className="status-badge">
                      {
                        site.is_active
                          ? "ACTIVE"
                          : "INACTIVE"
                      }
                    </span>
 
                  </td>
 
 
                  <td>
 
                    <div className="table-actions">
 
                      <button
                        type="button"
                        onClick={() =>
                          openEditForm(
                            site
                          )
                        }
                      >
                        Edit
                      </button>
 
                    </div>
 
                  </td>
 
                </tr>
 
              )
            )}
 
          </tbody>
 
        </table>
 
      </div>
 
 
      {
        filteredSites.length
        === 0
        && (
 
          <div className="empty-state">
            No sites found.
          </div>
 
        )
      }
 
    </div>
  );
}
 
 
function SiteInput({
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