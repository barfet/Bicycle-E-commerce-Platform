import apiClient from './api';

// Matches schemas.PartCategory
export interface PartCategory {
  id: number;
  name: string;
  display_order: number;
  product_type_id: number;
}

// Matches schemas.PartCategoryCreate
export interface PartCategoryCreateData {
  name: string;
  product_type_id: number;
  display_order?: number;
}

// Matches schemas.PartCategoryUpdate
export interface PartCategoryUpdateData {
  name?: string;
  display_order?: number;
  product_type_id?: number; // Allowing change?
}

// Fetch categories for a specific product type
export const fetchPartCategories = async (productTypeId: number): Promise<PartCategory[]> => {
  const response = await apiClient.get<PartCategory[]>('/admin/part-categories', {
    params: { product_type_id: productTypeId },
  });
  return response.data;
};

// Fetch a single category
export const fetchPartCategory = async (id: number): Promise<PartCategory> => {
  const response = await apiClient.get<PartCategory>(`/admin/part-categories/${id}`);
  return response.data;
};

// Create a new category
export const createPartCategory = async (data: PartCategoryCreateData): Promise<PartCategory> => {
  const response = await apiClient.post<PartCategory>('/admin/part-categories', data);
  return response.data;
};

// Update an existing category
export const updatePartCategory = async (id: number, data: Partial<PartCategoryUpdateData>): Promise<PartCategory> => {
  const response = await apiClient.put<PartCategory>(`/admin/part-categories/${id}`, data);
  return response.data;
};

// Delete a category
export const deletePartCategory = async (id: number): Promise<PartCategory> => {
  const response = await apiClient.delete<PartCategory>(`/admin/part-categories/${id}`);
  return response.data;
}; 