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
  createVisitor,
  deleteVisitor,
  getVisitors,
  updateVisitor,
} from "../../api/visitors.api";
 
import type {
  Visitor,
  CreateVisitorPayload,
} from "../../types/visitor";
 
 
const EMPTY_FORM: CreateVisitorPayload = {
  first_name: "",
  last_name: "",
  phone: "",
 
  middle_name: null,
  gender: null,
  date_of_birth: null,
 
  email: null,
  company: null,
  address: null,
  nationality: null,
 
  id_number: null,
  passport_number: null,
 
  vehicle_registration: null,
 
  is_blacklisted: false,
 
  notes: null,
};
 
 
function errorMessage(
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
      "Unable to complete the operation."
    );
  }
 
  return (
    "Unable to complete the operation."
  );
}
 
 
export function VisitorListPage() {
 
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
    editingVisitor,
    setEditingVisitor,
  ] = useState<Visitor | null>(
    null
  );
 
  const [
    form,
    setForm,
  ] = useState<CreateVisitorPayload>(
    EMPTY_FORM
  );
 
  const [
    formError,
    setFormError,
  ] = useState<string | null>(
    null
  );
 
 
  const {
    data: visitors = [],
    isLoading,
    isError,
  } = useQuery({
 
    queryKey: [
      "visitors",
    ],
 
    queryFn:
      getVisitors,
 
  });
 
 
  const saveMutation =
    useMutation({
 
      mutationFn: async () => {
 
        if (editingVisitor) {
 
          return updateVisitor(
            editingVisitor.id,
            form
          );
        }
 
        return createVisitor(
          form
        );
      },
 
 
      onSuccess: async () => {
 
        setFormError(null);
 
        closeForm();
 
        await queryClient
          .invalidateQueries({
            queryKey: [
              "visitors",
            ],
          });
      },
 
 
      onError: (error) => {
 
        setFormError(
          errorMessage(
            error
          )
        );
      },
 
    });
 
 
  const deleteMutation =
    useMutation({
 
      mutationFn:
        deleteVisitor,
 
      onSuccess: async () => {
 
        await queryClient
          .invalidateQueries({
            queryKey: [
              "visitors",
            ],
          });
      },
 
      onError: (error) => {
 
        window.alert(
          errorMessage(
            error
          )
        );
      },
 
    });
 
 
  const filteredVisitors =
    useMemo(() => {
 
      const term =
        search
          .trim()
          .toLowerCase();
 
      if (!term) {
        return visitors;
      }
 
      return visitors.filter(
        (visitor) => {
 
          const searchable = [
            visitor.first_name,
            visitor.middle_name,
            visitor.last_name,
            visitor.phone,
            visitor.email,
            visitor.company,
            visitor.id_number,
            visitor.passport_number,
            visitor.vehicle_registration,
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
      visitors,
      search,
    ]);
 
 
  function openCreateForm() {
 
    setEditingVisitor(
      null
    );
 
    setForm({
      ...EMPTY_FORM,
    });
 
    setFormError(null);
 
    setShowForm(true);
  }
 
 
  function openEditForm(
    visitor: Visitor
  ) {
 
    setEditingVisitor(
      visitor
    );
 
    setForm({
      first_name:
        visitor.first_name,
 
      middle_name:
        visitor.middle_name,
 
      last_name:
        visitor.last_name,
 
      gender:
        visitor.gender as
          | "Male"
          | "Female"
          | "Other"
          | null,
 
      date_of_birth:
        visitor.date_of_birth,
 
      phone:
        visitor.phone,
 
      email:
        visitor.email,
 
      company:
        visitor.company,
 
      address:
        visitor.address,
 
      nationality:
        visitor.nationality,
 
      id_number:
        visitor.id_number,
 
      passport_number:
        visitor.passport_number,
 
      vehicle_registration:
        visitor.vehicle_registration,
 
      photo_url:
        visitor.photo_url,
 
      is_blacklisted:
        visitor.is_blacklisted,
 
      notes:
        visitor.notes,
    });
 
    setFormError(null);
 
    setShowForm(true);
  }
 
 
  function closeForm() {
 
    setShowForm(false);
 
    setEditingVisitor(
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
      !form.first_name.trim()
      ||
      !form.last_name.trim()
      ||
      !form.phone.trim()
    ) {
 
      setFormError(
        "First name, last name and phone are required."
      );
 
      return;
    }
 
 
    saveMutation.mutate();
  }
 
 
  function setField<
    K extends keyof CreateVisitorPayload
  >(
    field: K,
    value: CreateVisitorPayload[K]
  ) {
 
    setForm(
      (current) => ({
        ...current,
        [field]: value,
      })
    );
  }
 
 
  if (isLoading) {
 
    return (
      <div>
        Loading visitors...
      </div>
    );
  }
 
 
  if (isError) {
 
    return (
      <div className="form-error">
        Unable to load visitors.
      </div>
    );
  }
 
 
  return (
    <div className="page">
 
      <div className="page-heading">
 
        <div>
 
          <h1>
            Visitors
          </h1>
 
          <p>
            Manage registered visitors
            and their identification
            details.
          </p>
 
        </div>
 
 
        <button
          type="button"
          className="button"
          onClick={
            openCreateForm
          }
        >
          Add Visitor
        </button>
 
      </div>
 
 
      <div className="list-toolbar">
 
        <input
          type="search"
          placeholder={
            "Search visitors..."
          }
          value={search}
          onChange={(event) =>
            setSearch(
              event.target.value
            )
          }
        />
 
      </div>
 
 
      {showForm && (
 
        <section className="detail-card visitor-form-card">
 
          <div className="section-heading">
 
            <h2>
              {
                editingVisitor
                  ? "Edit Visitor"
                  : "Add Visitor"
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
 
              <VisitorInput
                label="First Name *"
                value={
                  form.first_name
                }
                onChange={(value) =>
                  setField(
                    "first_name",
                    value
                  )
                }
              />
 
 
              <VisitorInput
                label="Middle Name"
                value={
                  form.middle_name
                  ?? ""
                }
                onChange={(value) =>
                  setField(
                    "middle_name",
                    value || null
                  )
                }
              />
 
 
              <VisitorInput
                label="Last Name *"
                value={
                  form.last_name
                }
                onChange={(value) =>
                  setField(
                    "last_name",
                    value
                  )
                }
              />
 
 
              <VisitorInput
                label="Phone *"
                value={
                  form.phone
                }
                onChange={(value) =>
                  setField(
                    "phone",
                    value
                  )
                }
              />
 
 
              <VisitorInput
                label="Email"
                type="email"
                value={
                  form.email ?? ""
                }
                onChange={(value) =>
                  setField(
                    "email",
                    value || null
                  )
                }
              />
 
 
              <VisitorInput
                label="Company"
                value={
                  form.company ?? ""
                }
                onChange={(value) =>
                  setField(
                    "company",
                    value || null
                  )
                }
              />
 
 
              <VisitorInput
                label="Nationality"
                value={
                  form.nationality
                  ?? ""
                }
                onChange={(value) =>
                  setField(
                    "nationality",
                    value || null
                  )
                }
              />
 
 
              <VisitorInput
                label="ID Number"
                value={
                  form.id_number
                  ?? ""
                }
                onChange={(value) =>
                  setField(
                    "id_number",
                    value || null
                  )
                }
              />
 
 
              <VisitorInput
                label="Passport Number"
                value={
                  form.passport_number
                  ?? ""
                }
                onChange={(value) =>
                  setField(
                    "passport_number",
                    value || null
                  )
                }
              />
 
 
              <VisitorInput
                label="Vehicle Registration"
                value={
                  form.vehicle_registration
                  ?? ""
                }
                onChange={(value) =>
                  setField(
                    "vehicle_registration",
                    value || null
                  )
                }
              />
 
            </div>
 
 
            <label className="checkbox-field">
 
              <input
                type="checkbox"
                checked={
                  form.is_blacklisted
                  ?? false
                }
                onChange={(event) =>
                  setField(
                    "is_blacklisted",
                    event.target.checked
                  )
                }
              />
 
              Blacklisted
 
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
                    editingVisitor
                      ? "Save Changes"
                      : "Create Visitor"
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
              <th>Visitor</th>
              <th>Phone</th>
              <th>Company</th>
              <th>ID / Passport</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
 
          </thead>
 
 
          <tbody>
 
            {filteredVisitors.map(
              (visitor) => (
 
                <tr key={visitor.id}>
 
                  <td>
 
                    <strong>
                      {
                        [
                          visitor.first_name,
                          visitor.middle_name,
                          visitor.last_name,
                        ]
                          .filter(Boolean)
                          .join(" ")
                      }
                    </strong>
 
                    <div className="table-secondary">
                      {
                        visitor.email
                        ?? "-"
                      }
                    </div>
 
                  </td>
 
 
                  <td>
                    {visitor.phone}
                  </td>
 
 
                  <td>
                    {
                      visitor.company
                      ?? "-"
                    }
                  </td>
 
 
                  <td>
                    {
                      visitor.id_number
                      ??
                      visitor.passport_number
                      ??
                      "-"
                    }
                  </td>
 
 
                  <td>
 
                    {
                      visitor.is_blacklisted
                        ? (
                          <span className="status-badge">
                            BLACKLISTED
                          </span>
                        )
                        : (
                          <span>
                            Active
                          </span>
                        )
                    }
 
                  </td>
 
 
                  <td>
 
                    <div className="table-actions">
 
                      <button
                        type="button"
                        onClick={() =>
                          openEditForm(
                            visitor
                          )
                        }
                      >
                        Edit
                      </button>
 
 
                      <button
                        type="button"
                        disabled={
                          deleteMutation
                            .isPending
                        }
                        onClick={() => {
 
                          const confirmed =
                            window.confirm(
                              `Delete ${visitor.first_name} ${visitor.last_name}?`
                            );
 
                          if (confirmed) {
 
                            deleteMutation
                              .mutate(
                                visitor.id
                              );
                          }
                        }}
                      >
                        Delete
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
        filteredVisitors.length
        === 0
        && (
 
          <div className="empty-state">
            No visitors found.
          </div>
 
        )
      }
 
    </div>
  );
}
 
 
function VisitorInput({
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