import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getHotels, createHotel, updateHotel, deleteHotel } from '../api/hotels';
import type { Hotel } from '../api/types';
import { MainLayout } from '../components/layout/MainLayout';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Loader } from '../components/common/Loader';
import { Modal } from '../components/common/Modal';
import { Input } from '../components/common/Input';
import { extractErrorMessage } from '../utils/errorHandlers';
import './HotelList.css';

export const HotelList: React.FC = () => {
    const [hotels, setHotels] = useState<Hotel[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [actionError, setActionError] = useState('');
    const [formError, setFormError] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingHotel, setEditingHotel] = useState<Hotel | null>(null);
    const [hotelName, setHotelName] = useState('');
    const [hotelLocation, setHotelLocation] = useState('');
    const [hotelActive, setHotelActive] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [deletingId, setDeletingId] = useState<number | null>(null);

    const navigate = useNavigate();

    useEffect(() => {
        const fetchHotels = async () => {
            try {
                const data = await getHotels();
                setHotels(data);
            } catch (err: any) {
                setError(extractErrorMessage(err, 'Failed to load hotels'));
            } finally {
                setLoading(false);
            }
        };

        fetchHotels();
    }, []);

    const openCreateModal = () => {
        setEditingHotel(null);
        setHotelName('');
        setHotelLocation('');
        setHotelActive(true);
        setFormError('');
        setIsModalOpen(true);
    };

    const openEditModal = (hotel: Hotel) => {
        setEditingHotel(hotel);
        setHotelName(hotel.name);
        setHotelLocation(hotel.location);
        setHotelActive(hotel.is_active);
        setFormError('');
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setEditingHotel(null);
        setFormError('');
    };

    const handleSubmitHotel = async (e: React.FormEvent) => {
        e.preventDefault();
        setFormError('');
        setSubmitting(true);

        try {
            if (editingHotel) {
                const updatedHotel = await updateHotel(editingHotel.id, {
                    name: hotelName.trim(),
                    location: hotelLocation.trim(),
                    is_active: hotelActive,
                });
                setHotels((prev) =>
                    prev.map((hotel) => (hotel.id === updatedHotel.id ? updatedHotel : hotel))
                );
            } else {
                const newHotel = await createHotel({
                    name: hotelName.trim(),
                    location: hotelLocation.trim(),
                    is_active: hotelActive,
                });
                setHotels((prev) => [newHotel, ...prev]);
            }
            closeModal();
        } catch (err: any) {
            setFormError(extractErrorMessage(err, 'Failed to save hotel'));
        } finally {
            setSubmitting(false);
        }
    };

    const handleDeleteHotel = async (hotel: Hotel) => {
        if (!window.confirm(`Delete ${hotel.name}? This cannot be undone.`)) {
            return;
        }

        setActionError('');
        setDeletingId(hotel.id);
        try {
            await deleteHotel(hotel.id);
            setHotels((prev) => prev.filter((item) => item.id !== hotel.id));
        } catch (err: any) {
            setActionError(extractErrorMessage(err, 'Failed to delete hotel'));
        } finally {
            setDeletingId(null);
        }
    };

    if (loading) {
        return (
            <MainLayout>
                <Loader text="Loading hotels..." />
            </MainLayout>
        );
    }

    if (error) {
        return (
            <MainLayout>
                <div className="error-message">{error}</div>
            </MainLayout>
        );
    }

    return (
        <MainLayout>
            <div className="hotel-list-container">
                <div className="hotel-list-header">
                    <div className="hotel-list-header__content">
                        <div>
                            <h1 className="hotel-list-title">Hotels</h1>
                            <p className="hotel-list-subtitle">Manage your hotel properties</p>
                        </div>
                        <Button variant="primary" onClick={openCreateModal}>
                            Add Hotel
                        </Button>
                    </div>
                    {actionError && <div className="action-message action-message--error">{actionError}</div>}
                </div>

                {hotels.length === 0 ? (
                    <Card>
                        <p className="empty-state">No hotels found. Create your first hotel to get started.</p>
                    </Card>
                ) : (
                    <div className="hotel-grid">
                        {hotels.map((hotel) => (
                            <Card key={hotel.id} hoverable>
                                <div className="hotel-card">
                                    <div className="hotel-card__content">
                                        <h3 className="hotel-card__title">{hotel.name}</h3>
                                        <p className="hotel-card__location">{hotel.location}</p>
                                        {hotel.is_active ? (
                                            <span className="hotel-card__badge hotel-card__badge--active">Active</span>
                                        ) : (
                                            <span className="hotel-card__badge hotel-card__badge--inactive">Inactive</span>
                                        )}
                                    </div>
                                    <div className="hotel-card__actions">
                                        <Button variant="primary" onClick={() => navigate(`/hotels/${hotel.id}`)}>
                                            View Details
                                        </Button>
                                        <Button variant="secondary" onClick={() => openEditModal(hotel)}>
                                            Edit
                                        </Button>
                                        <Button
                                            variant="outline"
                                            onClick={() => handleDeleteHotel(hotel)}
                                            disabled={deletingId === hotel.id}
                                        >
                                            {deletingId === hotel.id ? 'Deleting...' : 'Delete'}
                                        </Button>
                                    </div>
                                </div>
                            </Card>
                        ))}
                    </div>
                )}
            </div>

            <Modal
                isOpen={isModalOpen}
                onClose={closeModal}
                title={editingHotel ? 'Edit Hotel' : 'Add Hotel'}
            >
                <form onSubmit={handleSubmitHotel} className="hotel-form">
                    <Input
                        label="Hotel Name"
                        type="text"
                        value={hotelName}
                        onChange={(e) => setHotelName(e.target.value)}
                        placeholder="Hotel name"
                        required
                        fullWidth
                    />
                    <Input
                        label="Location"
                        type="text"
                        value={hotelLocation}
                        onChange={(e) => setHotelLocation(e.target.value)}
                        placeholder="City, Country"
                        required
                        fullWidth
                    />
                    <label className="hotel-form__checkbox">
                        <input
                            type="checkbox"
                            checked={hotelActive}
                            onChange={(e) => setHotelActive(e.target.checked)}
                        />
                        Active
                    </label>
                    {formError && <div className="action-message action-message--error">{formError}</div>}
                    <div className="hotel-form__actions">
                        <Button type="button" variant="ghost" onClick={closeModal} disabled={submitting}>
                            Cancel
                        </Button>
                        <Button type="submit" variant="primary" loading={submitting}>
                            {editingHotel ? 'Save Changes' : 'Create Hotel'}
                        </Button>
                    </div>
                </form>
            </Modal>
        </MainLayout>
    );
};
