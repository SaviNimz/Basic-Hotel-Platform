import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getHotel, getRoomTypes } from '../api/hotels';
import {
    createRateAdjustment,
    createRoomType,
    updateRoomType,
    deleteRoomType,
    getEffectiveRate,
    getRateAdjustmentsByRoomType,
} from '../api/rooms';
import type {
    Hotel,
    RoomType,
    RateAdjustmentCreate,
    EffectiveRateResponse,
    RateAdjustment,
} from '../api/types';
import { MainLayout } from '../components/layout/MainLayout';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Loader } from '../components/common/Loader';
import { Modal } from '../components/common/Modal';
import { Input } from '../components/common/Input';
import { RateAdjustmentHistoryModal } from '../components/rooms/RateAdjustmentHistoryModal';
import './HotelDetail.css';

export const HotelDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [hotel, setHotel] = useState<Hotel | null>(null);
    const [roomTypes, setRoomTypes] = useState<RoomType[]>([]);
    const [effectiveRates, setEffectiveRates] = useState<Record<number, EffectiveRateResponse>>({});
    const [rateAdjustments, setRateAdjustments] = useState<Record<number, RateAdjustment[]>>({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [deletingRoomTypeId, setDeletingRoomTypeId] = useState<number | null>(null);

    // Room type modal state
    const [isRoomTypeModalOpen, setIsRoomTypeModalOpen] = useState(false);
    const [editingRoomType, setEditingRoomType] = useState<RoomType | null>(null);
    const [roomTypeName, setRoomTypeName] = useState('');
    const [roomTypeRate, setRoomTypeRate] = useState('');
    const [roomTypeError, setRoomTypeError] = useState('');
    const [roomTypeSubmitting, setRoomTypeSubmitting] = useState(false);

    // Rate adjustment modal state
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedRoomType, setSelectedRoomType] = useState<RoomType | null>(null);
    const [adjustmentAmount, setAdjustmentAmount] = useState('');
    const [effectiveDate, setEffectiveDate] = useState('');
    const [reason, setReason] = useState('');
    const [adjustmentError, setAdjustmentError] = useState('');
    const [submitting, setSubmitting] = useState(false);

    // Rate adjustment history modal
    const [historyRoomType, setHistoryRoomType] = useState<RoomType | null>(null);
    const [isHistoryModalOpen, setIsHistoryModalOpen] = useState(false);
    const [historyLoading, setHistoryLoading] = useState(false);
    const [historyError, setHistoryError] = useState('');

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
                const rateResponses = await Promise.all(
                    roomTypesData.map(async (roomType) => {
                        try {
                            return await getEffectiveRate(roomType.id);
                        } catch {
                            return null;
                        }
                    })
                );
                const rateMap = rateResponses.reduce<Record<number, EffectiveRateResponse>>((acc, rate) => {
                    if (rate) {
                        acc[rate.room_type_id] = rate;
                    }
                    return acc;
                }, {});
                setEffectiveRates(rateMap);
            } catch (err: any) {
                setError(err.response?.data?.detail || 'Failed to load hotel details');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [id]);

    const openRoomTypeModal = (roomType?: RoomType) => {
        setEditingRoomType(roomType || null);
        setRoomTypeName(roomType?.name ?? '');
        setRoomTypeRate(roomType ? roomType.base_rate.toString() : '');
        setRoomTypeError('');
        setIsRoomTypeModalOpen(true);
    };

    const closeRoomTypeModal = () => {
        setIsRoomTypeModalOpen(false);
        setEditingRoomType(null);
        setRoomTypeError('');
    };

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

    const closeHistoryModal = () => {
        setIsHistoryModalOpen(false);
        setHistoryRoomType(null);
        setHistoryError('');
    };

    const fetchEffectiveRate = async (roomTypeId: number, date?: string) => {
        try {
            const rate = await getEffectiveRate(roomTypeId, date);
            setEffectiveRates((prev) => ({ ...prev, [roomTypeId]: rate }));
        } catch {
            return;
        }
    };

    const fetchRateAdjustments = async (roomTypeId: number) => {
        const adjustments = await getRateAdjustmentsByRoomType(roomTypeId);
        setRateAdjustments((prev) => ({ ...prev, [roomTypeId]: adjustments }));
        return adjustments;
    };

    const openHistoryModal = async (roomType: RoomType) => {
        setHistoryRoomType(roomType);
        setIsHistoryModalOpen(true);
        setHistoryLoading(true);
        setHistoryError('');

        try {
            await fetchRateAdjustments(roomType.id);
        } catch (err: any) {
            setHistoryError(err.response?.data?.detail || 'Failed to load rate history');
        } finally {
            setHistoryLoading(false);
        }
    };

    const handleDeleteRoomType = async (roomType: RoomType) => {
        if (!window.confirm(`Delete ${roomType.name}? This cannot be undone.`)) {
            return;
        }
        setDeletingRoomTypeId(roomType.id);
        try {
            await deleteRoomType(roomType.id);
            setRoomTypes((prev) => prev.filter((item) => item.id !== roomType.id));
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to delete room type');
        } finally {
            setDeletingRoomTypeId(null);
        }
    };

    const handleSubmitRoomType = async (e: React.FormEvent) => {
        e.preventDefault();
        setRoomTypeError('');

        if (!hotel) return;

        const baseRate = parseFloat(roomTypeRate);
        if (isNaN(baseRate) || baseRate <= 0) {
            setRoomTypeError('Please enter a valid base rate greater than 0');
            return;
        }

        setRoomTypeSubmitting(true);

        try {
            if (editingRoomType) {
                const updatedRoomType = await updateRoomType(editingRoomType.id, {
                    name: roomTypeName.trim(),
                    base_rate: baseRate,
                    hotel_id: hotel.id,
                });
                setRoomTypes((prev) =>
                    prev.map((roomType) =>
                        roomType.id === updatedRoomType.id ? updatedRoomType : roomType
                    )
                );
                await fetchEffectiveRate(updatedRoomType.id);
            } else {
                const newRoomType = await createRoomType({
                    name: roomTypeName.trim(),
                    base_rate: baseRate,
                    hotel_id: hotel.id,
                });
                setRoomTypes((prev) => [...prev, newRoomType]);
                await fetchEffectiveRate(newRoomType.id);
            }
            closeRoomTypeModal();
        } catch (err: any) {
            const detail = err.response?.data?.detail;
            if (typeof detail === 'string') {
                setRoomTypeError(detail);
            } else if (Array.isArray(detail)) {
                setRoomTypeError(detail.map((e: any) => e.msg).join(', '));
            } else {
                setRoomTypeError('Failed to save room type');
            }
        } finally {
            setRoomTypeSubmitting(false);
        }
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

            await fetchEffectiveRate(selectedRoomType.id, effectiveDate);
            await fetchRateAdjustments(selectedRoomType.id);

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
                    <div className="room-types-header">
                        <h2 className="section-title">Room Types</h2>
                        <Button variant="primary" onClick={() => openRoomTypeModal()}>
                            Add Room Type
                        </Button>
                    </div>

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
                                            {effectiveRates[roomType.id] && (
                                                <div className="room-type-card__rate room-type-card__rate--effective">
                                                    <span className="room-type-card__rate-label">
                                                        Effective Rate ({effectiveRates[roomType.id].effective_date}):
                                                    </span>
                                                    <span className="room-type-card__rate-value">
                                                        ${effectiveRates[roomType.id].effective_rate.toFixed(2)}
                                                    </span>
                                                </div>
                                            )}
                                        </div>
                                        <div className="room-type-card__actions">
                                            <Button
                                                variant="secondary"
                                                size="sm"
                                                onClick={() => openRoomTypeModal(roomType)}
                                            >
                                                Edit
                                            </Button>
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={() => handleDeleteRoomType(roomType)}
                                                disabled={deletingRoomTypeId === roomType.id}
                                            >
                                                {deletingRoomTypeId === roomType.id ? 'Deleting...' : 'Delete'}
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="sm"
                                                onClick={() => openHistoryModal(roomType)}
                                            >
                                                History
                                            </Button>
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

            <RateAdjustmentHistoryModal
                isOpen={isHistoryModalOpen}
                roomType={historyRoomType}
                adjustments={
                    historyRoomType ? rateAdjustments[historyRoomType.id] ?? [] : []
                }
                loading={historyLoading}
                error={historyError}
                onClose={closeHistoryModal}
            />

            {/* Room Type Modal */}
            <Modal
                isOpen={isRoomTypeModalOpen}
                onClose={closeRoomTypeModal}
                title={editingRoomType ? 'Edit Room Type' : 'Add Room Type'}
            >
                <form onSubmit={handleSubmitRoomType} className="room-type-form">
                    <Input
                        label="Room Type Name"
                        type="text"
                        value={roomTypeName}
                        onChange={(e) => setRoomTypeName(e.target.value)}
                        placeholder="e.g., Deluxe Suite"
                        required
                        fullWidth
                    />
                    <Input
                        label="Base Rate"
                        type="number"
                        step="0.01"
                        min="0.01"
                        value={roomTypeRate}
                        onChange={(e) => setRoomTypeRate(e.target.value)}
                        placeholder="e.g., 150.00"
                        required
                        fullWidth
                    />

                    {roomTypeError && <div className="adjustment-error">{roomTypeError}</div>}

                    <div className="adjustment-form-actions">
                        <Button
                            type="button"
                            variant="ghost"
                            onClick={closeRoomTypeModal}
                            disabled={roomTypeSubmitting}
                        >
                            Cancel
                        </Button>
                        <Button type="submit" variant="primary" loading={roomTypeSubmitting}>
                            {editingRoomType ? 'Save Changes' : 'Create Room Type'}
                        </Button>
                    </div>
                </form>
            </Modal>
        </MainLayout>
    );
};
