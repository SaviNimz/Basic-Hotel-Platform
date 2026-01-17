import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getHotel, getRoomTypes } from '../api/hotels';
import { createRateAdjustment } from '../api/rooms';
import type { Hotel, RoomType, RateAdjustmentCreate } from '../api/types';
import { MainLayout } from '../components/layout/MainLayout';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Loader } from '../components/common/Loader';
import { Modal } from '../components/common/Modal';
import { Input } from '../components/common/Input';
import './HotelDetail.css';

export const HotelDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [hotel, setHotel] = useState<Hotel | null>(null);
    const [roomTypes, setRoomTypes] = useState<RoomType[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    // Rate adjustment modal state
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedRoomType, setSelectedRoomType] = useState<RoomType | null>(null);
    const [adjustmentAmount, setAdjustmentAmount] = useState('');
    const [effectiveDate, setEffectiveDate] = useState('');
    const [reason, setReason] = useState('');
    const [adjustmentError, setAdjustmentError] = useState('');
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            if (!id) return;

            try {
                const [hotelData, roomTypesData] = await Promise.all([
                    getHotel(parseInt(id)),
                    getRoomTypes(parseInt(id)),
                ]);
                setHotel(hotelData);
                setRoomTypes(roomTypesData);
            } catch (err: any) {
                setError(err.response?.data?.detail || 'Failed to load hotel details');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [id]);

    const openAdjustmentModal = (roomType: RoomType) => {
        setSelectedRoomType(roomType);
        setIsModalOpen(true);
        setAdjustmentAmount('');
        setEffectiveDate('');
        setReason('');
        setAdjustmentError('');
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setSelectedRoomType(null);
    };

    const handleSubmitAdjustment = async (e: React.FormEvent) => {
        e.preventDefault();
        setAdjustmentError('');

        if (!selectedRoomType) return;

        const amount = parseFloat(adjustmentAmount);
        if (isNaN(amount)) {
            setAdjustmentError('Please enter a valid adjustment amount');
            return;
        }

        setSubmitting(true);

        try {
            const adjustment: RateAdjustmentCreate = {
                room_type_id: selectedRoomType.id,
                adjustment_amount: amount,
                effective_date: effectiveDate,
                reason: reason.trim(),
            };

            await createRateAdjustment(adjustment);

            // Success - close modal and show success (could add toast notification)
            closeModal();
            alert('Rate adjustment created successfully!');
        } catch (err: any) {
            const detail = err.response?.data?.detail;
            if (typeof detail === 'string') {
                setAdjustmentError(detail);
            } else if (Array.isArray(detail)) {
                setAdjustmentError(detail.map((e: any) => e.msg).join(', '));
            } else {
                setAdjustmentError('Failed to create rate adjustment');
            }
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) {
        return (
            <MainLayout>
                <Loader text="Loading hotel details..." />
            </MainLayout>
        );
    }

    if (error || !hotel) {
        return (
            <MainLayout>
                <div className="error-message">{error || 'Hotel not found'}</div>
            </MainLayout>
        );
    }

    return (
        <MainLayout>
            <div className="hotel-detail-container">
                {/* Hotel Info */}
                <Card className="hotel-info">
                    <h1 className="hotel-detail-title">{hotel.name}</h1>
                    <p className="hotel-detail-location">{hotel.location}</p>
                    {hotel.is_active ? (
                        <span className="hotel-badge hotel-badge--active">Active</span>
                    ) : (
                        <span className="hotel-badge hotel-badge--inactive">Inactive</span>
                    )}
                </Card>

                {/* Room Types */}
                <div className="room-types-section">
                    <h2 className="section-title">Room Types</h2>

                    {roomTypes.length === 0 ? (
                        <Card>
                            <p className="empty-state">No room types available for this hotel.</p>
                        </Card>
                    ) : (
                        <div className="room-types-grid">
                            {roomTypes.map((roomType) => (
                                <Card key={roomType.id}>
                                    <div className="room-type-card">
                                        <div className="room-type-card__content">
                                            <h3 className="room-type-card__name">{roomType.name}</h3>
                                            <div className="room-type-card__rate">
                                                <span className="room-type-card__rate-label">Base Rate:</span>
                                                <span className="room-type-card__rate-value">
                                                    ${roomType.base_rate.toFixed(2)}
                                                </span>
                                            </div>
                                        </div>
                                        <div className="room-type-card__actions">
                                            <Button
                                                variant="primary"
                                                size="sm"
                                                onClick={() => openAdjustmentModal(roomType)}
                                            >
                                                Adjust Rate
                                            </Button>
                                        </div>
                                    </div>
                                </Card>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* Rate Adjustment Modal */}
            <Modal
                isOpen={isModalOpen}
                onClose={closeModal}
                title={`Adjust Rate - ${selectedRoomType?.name}`}
            >
                <form onSubmit={handleSubmitAdjustment} className="adjustment-form">
                    <Input
                        label="Adjustment Amount"
                        type="number"
                        step="0.01"
                        value={adjustmentAmount}
                        onChange={(e) => setAdjustmentAmount(e.target.value)}
                        placeholder="e.g., 10.00 or -5.00"
                        required
                        fullWidth
                    />

                    <Input
                        label="Effective Date"
                        type="date"
                        value={effectiveDate}
                        onChange={(e) => setEffectiveDate(e.target.value)}
                        required
                        fullWidth
                    />

                    <Input
                        label="Reason"
                        type="text"
                        value={reason}
                        onChange={(e) => setReason(e.target.value)}
                        placeholder="Reason for adjustment"
                        required
                        fullWidth
                    />

                    {adjustmentError && <div className="adjustment-error">{adjustmentError}</div>}

                    <div className="adjustment-form-actions">
                        <Button type="button" variant="ghost" onClick={closeModal} disabled={submitting}>
                            Cancel
                        </Button>
                        <Button type="submit" variant="primary" loading={submitting}>
                            Submit Adjustment
                        </Button>
                    </div>
                </form>
            </Modal>
        </MainLayout>
    );
};
