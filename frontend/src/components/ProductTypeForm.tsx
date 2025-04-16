import React, { useState, useEffect } from 'react';
import useAdminStore from '../store/useAdminStore';
import { ProductType, ProductTypeData } from '../services/productTypeService';

interface ProductTypeFormProps {
  initialData?: ProductType | null; // Provide data for editing
  onSave: () => void; // Callback after successful save
  onCancel: () => void; // Callback to close the form/modal
}

const ProductTypeForm: React.FC<ProductTypeFormProps> = ({ initialData, onSave, onCancel }) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [formError, setFormError] = useState<string | null>(null);

  const { 
    addProductType, 
    editProductType, 
    productTypeLoading: loading,
    productTypeError: storeError
  } = useAdminStore();

  const isEditing = Boolean(initialData);

  useEffect(() => {
    // Pre-fill form if editing
    if (initialData) {
      setName(initialData.name);
      setDescription(initialData.description || '');
    }
  }, [initialData]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError(null); // Clear previous form error

    const productTypeData: ProductTypeData = {
      name,
      description: description || null, // Send null if empty
    };

    try {
      if (isEditing && initialData) {
        await editProductType(initialData.id, productTypeData);
      } else {
        await addProductType(productTypeData);
      }
      onSave(); // Call success callback
    } catch (err: any) {
      // Error is already set in the store, but we can show it specifically in the form
      console.error("Form submission error:", err);
      // Use the error message from the store if available
      setFormError(storeError || 'An unexpected error occurred.');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ padding: '1rem', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: 'white' }}>
      <h3>{isEditing ? 'Edit Product Type' : 'Add New Product Type'}</h3>
      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="pt-name">Name:</label>
        <input
          type="text"
          id="pt-name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={{ width: '100%', padding: '0.5rem', boxSizing: 'border-box' }}
        />
      </div>
      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="pt-description">Description:</label>
        <textarea
          id="pt-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          style={{ width: '100%', padding: '0.5rem', boxSizing: 'border-box' }}
        />
      </div>
      {formError && <p style={{ color: 'red', marginBottom: '1rem' }}>{formError}</p>}
      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
        <button type="button" onClick={onCancel} disabled={loading}>
          Cancel
        </button>
        <button type="submit" disabled={loading}>
          {loading ? 'Saving...' : (isEditing ? 'Update' : 'Create')}
        </button>
      </div>
    </form>
  );
};

export default ProductTypeForm; 