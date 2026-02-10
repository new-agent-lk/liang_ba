import request from "@/utils/request";

// Company Info API
export const getCompanyInfo = () => {
  return request.get("/api/admin/company-info/");
};

export const updateCompanyInfo = (data: any) => {
  return request.patch("/api/admin/company-info/", data);
};
