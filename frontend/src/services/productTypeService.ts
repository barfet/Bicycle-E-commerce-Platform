import apiClient from './api';

// Define the shape of the Product Type data expected from the API
// Match this with the backend schemas.ProductType
export interface ProductType {
  id: number;
  name: string;
  description: string | null;
  // Add created_at, updated_at if needed in the UI
}

// Define the shape for creating/updating
// Match backend schemas.ProductTypeCreate / ProductTypeUpdate
export interface ProductTypeData {
  name: string;
  description?: string | null;
}

// Fetch all product types
export const fetchProductTypes = async (): Promise<ProductType[]> => {
  const response = await apiClient.get<ProductType[]>('/admin/product-types');
  return response.data;
};

// Fetch a single product type
export const fetchProductType = async (id: number): Promise<ProductType> => {
  const response = await apiClient.get<ProductType>(`/admin/product-types/${id}`);
  return response.data;
};

// Create a new product type
export const createProductType = async (data: ProductTypeData): Promise<ProductType> => {
  const response = await apiClient.post<ProductType>('/admin/product-types', data);
  return response.data;
};

// Update an existing product type
export const updateProductType = async (id: number, data: Partial<ProductTypeData>): Promise<ProductType> => {
  const response = await apiClient.put<ProductType>(`/admin/product-types/${id}`, data);
  return response.data;
};

// Delete a product type
export const deleteProductType = async (id: number): Promise<ProductType> => {
  const response = await apiClient.delete<ProductType>(`/admin/product-types/${id}`);
  return response.data;
}; 