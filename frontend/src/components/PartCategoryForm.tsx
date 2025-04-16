import React, { useState, useEffect } from 'react';
import useAdminStore from '../store/useAdminStore';
import { PartCategory, PartCategoryCreateData, PartCategoryUpdateData } from '../services/partCategoryService';

interface PartCategoryFormProps {
  productTypeId: number; // Category must belong to a product type
  initialData?: PartCategory | null;
  onSave: () => void;
  onCancel: () => void;
}

const PartCategoryForm: React.FC<PartCategoryFormProps> = ({ productTypeId, initialData, onSave, onCancel }) => {
  const [name, setName] = useState('');
  const [displayOrder, setDisplayOrder] = useState<number>(0);
  const [formError, setFormError] = useState<string | null>(null);

  const { addPartCategory, editPartCategory, partCategoryLoading: loading, partCategoryError: storeError } = useAdminStore();

  const isEditing = Boolean(initialData);

  useEffect(() => {
    if (initialData) {
      setName(initialData.name);
      setDisplayOrder(initialData.display_order || 0);
    }
  }, [initialData]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError(null);

    try {
      if (isEditing && initialData) {
        const updateData: PartCategoryUpdateData = {
          name: name !== initialData.name ? name : undefined,
          display_order: displayOrder !== initialData.display_order ? displayOrder : undefined,
          // Not allowing productTypeId change in this form for simplicity
        };
        // Only send changed data
        const changedData = Object.entries(updateData).reduce((acc, [key, value]) => {
          if (value !== undefined) {
            acc[key as keyof PartCategoryUpdateData] = value;
          }
          return acc;
        }, {} as Partial<PartCategoryUpdateData>);

        if (Object.keys(changedData).length > 0) {
            await editPartCategory(initialData.id, changedData);
        }
      } else {
        const createData: PartCategoryCreateData = {
          name,
          display_order: displayOrder,
          product_type_id: productTypeId, // Use the passed productTypeId
        };
        await addPartCategory(createData);
      }
      onSave();
    } catch (err: any) {
      console.error("Part Category form error:", err);
      setFormError(storeError || 'An unexpected error occurred.');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ padding: '1rem', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: 'white', minWidth: '350px' }}>
      <h3>{isEditing ? 'Edit Part Category' : 'Add New Part Category'}</h3>
      <p>For Product Type ID: {productTypeId}</p>
      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="pc-name">Name:</label>
        <input
          type="text"
          id="pc-name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={{ width: '100%', padding: '0.5rem', boxSizing: 'border-box' }}
        />
      </div>
      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="pc-display-order">Display Order:</label>
        <input
          type="number"
          id="pc-display-order"
          value={displayOrder}
          onChange={(e) => setDisplayOrder(parseInt(e.target.value, 10) || 0)}
          required
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

export default PartCategoryForm; 