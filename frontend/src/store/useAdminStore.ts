import { create } from 'zustand';
import {
  ProductType,
  ProductTypeData,
  fetchProductTypes,
  createProductType,
  updateProductType,
  deleteProductType,
} from '../services/productTypeService';
import {
  PartCategory,
  PartCategoryCreateData,
  PartCategoryUpdateData,
  fetchPartCategories,
  createPartCategory,
  updatePartCategory,
  deletePartCategory,
} from '../services/partCategoryService';

// Combined state for Admin Panel
interface AdminState {
  // Product Type State
  productTypes: ProductType[];
  productTypeLoading: boolean;
  productTypeError: string | null;
  fetchProductTypes: () => Promise<void>;
  addProductType: (data: ProductTypeData) => Promise<void>;
  editProductType: (id: number, data: Partial<ProductTypeData>) => Promise<void>;
  removeProductType: (id: number) => Promise<void>;

  // Part Category State (tied to selected Product Type)
  selectedProductTypeId: number | null;
  partCategories: PartCategory[];
  partCategoryLoading: boolean;
  partCategoryError: string | null;
  selectProductType: (id: number | null) => Promise<void>;
  addPartCategory: (data: PartCategoryCreateData) => Promise<void>;
  editPartCategory: (id: number, data: Partial<PartCategoryUpdateData>) => Promise<void>;
  removePartCategory: (id: number) => Promise<void>;
}

const useAdminStore = create<AdminState>((set, get) => ({
  // --- Initial Product Type State ---
  productTypes: [],
  productTypeLoading: false,
  productTypeError: null,

  // --- Initial Part Category State ---
  selectedProductTypeId: null,
  partCategories: [],
  partCategoryLoading: false,
  partCategoryError: null,

  // --- Product Type Actions ---
  fetchProductTypes: async () => {
    set({ productTypeLoading: true, productTypeError: null });
    try {
      const data = await fetchProductTypes();
      set({ productTypes: data, productTypeLoading: false });
    } catch (err: any) {
      console.error("Error fetching product types:", err);
      set({ productTypeError: 'Failed to fetch product types', productTypeLoading: false });
    }
  },

  addProductType: async (data) => {
    set({ productTypeLoading: true, productTypeError: null });
    try {
      const newProductType = await createProductType(data);
      set((state) => ({
        productTypes: [...state.productTypes, newProductType],
        productTypeLoading: false,
      }));
    } catch (err: any) {
      console.error("Error adding product type:", err);
      let errorMsg = 'Failed to add product type';
      if (err.response && err.response.status === 409) {
        errorMsg = err.response.data.detail || 'Product type name already exists.';
      }
      set({ productTypeError: errorMsg, productTypeLoading: false });
      throw err;
    }
  },

  editProductType: async (id, data) => {
    set({ productTypeLoading: true, productTypeError: null });
    try {
      const updatedProductType = await updateProductType(id, data);
      set((state) => ({
        productTypes: state.productTypes.map((pt) =>
          pt.id === id ? updatedProductType : pt
        ),
        productTypeLoading: false,
      }));
    } catch (err: any) {
      console.error("Error updating product type:", err);
      set({ productTypeError: 'Failed to update product type', productTypeLoading: false });
      throw err;
    }
  },

  removeProductType: async (id) => {
    set({ productTypeLoading: true, productTypeError: null });
    try {
      await deleteProductType(id);
      set((state) => ({
        productTypes: state.productTypes.filter((pt) => pt.id !== id),
        selectedProductTypeId: state.selectedProductTypeId === id ? null : state.selectedProductTypeId,
        partCategories: state.selectedProductTypeId === id ? [] : state.partCategories,
        productTypeLoading: false,
      }));
    } catch (err: any) {
      console.error("Error deleting product type:", err);
      set({ productTypeError: 'Failed to delete product type', productTypeLoading: false });
    }
  },

  // --- Part Category Actions ---
  selectProductType: async (id) => {
    if (id === null) {
      set({ selectedProductTypeId: null, partCategories: [], partCategoryError: null });
      return;
    }
    set({ selectedProductTypeId: id, partCategoryLoading: true, partCategoryError: null });
    try {
      const data = await fetchPartCategories(id);
      set({ partCategories: data, partCategoryLoading: false });
    } catch (err: any) {
      console.error(`Error fetching part categories for product type ${id}:`, err);
      set({ partCategoryError: 'Failed to fetch part categories', partCategoryLoading: false, partCategories: [] });
    }
  },

  addPartCategory: async (data) => {
    set({ partCategoryLoading: true, partCategoryError: null });
    try {
      const newCategory = await createPartCategory(data);
      set((state) => ({
        partCategories: state.selectedProductTypeId === data.product_type_id
          ? [...state.partCategories, newCategory]
          : state.partCategories,
        partCategoryLoading: false,
      }));
    } catch (err: any) {
      console.error("Error adding part category:", err);
      let errorMsg = 'Failed to add part category';
      if (err.response && err.response.status === 409) {
        errorMsg = err.response.data.detail || 'Part category creation failed. Check constraints.';
      }
      set({ partCategoryError: errorMsg, partCategoryLoading: false });
      throw err;
    }
  },

  editPartCategory: async (id, data) => {
    set({ partCategoryLoading: true, partCategoryError: null });
    try {
      const updatedCategory = await updatePartCategory(id, data);
      set((state) => ({
        partCategories: state.partCategories.map((pc) =>
          pc.id === id ? updatedCategory : pc
        ),
        partCategoryLoading: false,
      }));
    } catch (err: any) {
      console.error("Error updating part category:", err);
      set({ partCategoryError: 'Failed to update part category', partCategoryLoading: false });
      throw err;
    }
  },

  removePartCategory: async (id) => {
    set({ partCategoryLoading: true, partCategoryError: null });
    try {
      await deletePartCategory(id);
      set((state) => ({
        partCategories: state.partCategories.filter((pc) => pc.id !== id),
        partCategoryLoading: false,
      }));
    } catch (err: any) {
      console.error("Error deleting part category:", err);
      set({ partCategoryError: 'Failed to delete part category', partCategoryLoading: false });
    }
  },
}));

export default useAdminStore; 