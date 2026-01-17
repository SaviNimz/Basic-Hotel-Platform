import React, { useEffect, useMemo, useState } from 'react';
import { getHotels, getRoomTypes } from '../api/hotels';
import { createRateAdjustment, getRateAdjustmentsByRoomType } from '../api/rooms';
import type { Hotel, RateAdjustment, RoomType } from '../api/types';
import { MainLayout } from '../components/layout/MainLayout';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Input } from '../components/common/Input';
import { Loader } from '../components/common/Loader';
import { extractErrorMessage } from '../utils/errorHandlers';
import { parseFloatValue } from '../utils/validators';
import './RateAdjustments.css';

export const RateAdjustments: React.FC = () => {
    const [hotels, setHotels] = useState<Hotel[]>([]);
    const [roomTypes, setRoomTypes] = useState<RoomType[]>([]);
    const [adjustments, setAdjustments] = useState<RateAdjustment[]>([]);
    const [selectedHotelId, setSelectedHotelId] = useState<number | null>(null);
    const [selectedRoomTypeId, setSelectedRoomTypeId] = useState<number | null>(null);
    const [loadingHotels, setLoadingHotels] = useState(true);
    const [loadingRoomTypes, setLoadingRoomTypes] = useState(false);
    const [loadingAdjustments, setLoadingAdjustments] = useState(false);
    const [error, setError] = useState('');

    const [amount, setAmount] = useState('');
    const [effectiveDate, setEffectiveDate] = useState('');
    const [reason, setReason] = useState('');
    const [formError, setFormError] = useState('');
    const [submitting, setSubmitting] = useState(false);

    const selectedHotel = useMemo(
        () => hotels.find((hotel) => hotel.id === selectedHotelId) ?? null,
        [hotels, selectedHotelId]
    );

    const selectedRoomType = useMemo(
        () => roomTypes.find((room) => room.id === selectedRoomTypeId) ?? null,
        [roomTypes, selectedRoomTypeId]
    );

    useEffect(() => {
        const fetchHotels = async () => {
            try {
                const data = await getHotels();
                setHotels(data);
                if (data.length > 0) {
                    setSelectedHotelId(data[0].id);
                }
            } catch (err: any) {
                setError(extractErrorMessage(err, 'Failed to load hotels'));
            } finally {
                setLoadingHotels(false);
            }
        };

        fetchHotels();
    }, []);

    useEffect(() => {
        const fetchRoomTypes = async () => {
            if (!selectedHotelId) {
                setRoomTypes([]);
                return;
            }

            setLoadingRoomTypes(true);
            setError('');
            try {
                const data = await getRoomTypes(selectedHotelId);
                setRoomTypes(data);
                setSelectedRoomTypeId(data[0]?.id ?? null);
            } catch (err: any) {
                setError(extractErrorMessage(err, 'Failed to load room types'));
            } finally {
                setLoadingRoomTypes(false);
            }
        };

        fetchRoomTypes();
    }, [selectedHotelId]);

    useEffect(() => {
        const fetchAdjustments = async () => {
            if (!selectedRoomTypeId) {
                setAdjustments([]);
                return;
            }

            setLoadingAdjustments(true);
            setError('');
            try {
                const data = await getRateAdjustmentsByRoomType(selectedRoomTypeId);
                setAdjustments(data);
            } catch (err: any) {
                setError(extractErrorMessage(err, 'Failed to load rate adjustments'));
            } finally {
                setLoadingAdjustments(false);
            }
        };

        fetchAdjustments();
    }, [selectedRoomTypeId]);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setFormError('');

        if (!selectedRoomType) {
            setFormError('Select a room type before submitting.');
            return;
        }

        const validation = parseFloatValue(amount, 'adjustment amount');
        if (validation.error) {
            setFormError(validation.error);
            return;
        }

        setSubmitting(true);
        try {
            await createRateAdjustment({
                room_type_id: selectedRoomType.id,
                adjustment_amount: validation.value!,
                effective_date: effectiveDate,
                reason: reason.trim(),
            });
            const updatedAdjustments = await getRateAdjustmentsByRoomType(selectedRoomType.id);
            setAdjustments(updatedAdjustments);
            setAmount('');
            setEffectiveDate('');
            setReason('');
        } catch (err: any) {
            setFormError(extractErrorMessage(err, 'Failed to create rate adjustment'));
        } finally {
            setSubmitting(false);
        }
    };

    if (loadingHotels) {
        return (
            <MainLayout>
                <Loader text="Loading rate adjustments..." />
            </MainLayout>
        );
    }

    return (
        <MainLayout>
            <div className="rate-adjustments-page">
                <div className="rate-adjustments-header">
                    <div>
                        <h1 className="rate-adjustments-title">Rate Adjustments</h1>
                        <p className="rate-adjustments-subtitle">
                            Manage date-specific rate changes for any room type.
                        </p>
                    </div>
                </div>

                {error && <div className="rate-adjustments-error">{error}</div>}

                <div className="rate-adjustments-grid">
                    <Card>
                        <h2 className="rate-adjustments-section-title">Create Adjustment</h2>
                        <form className="rate-adjustments-form" onSubmit={handleSubmit}>
                            <label className="rate-adjustments-label">
                                Hotel
                                <select
                                    value={selectedHotelId ?? ''}
                                    onChange={(event) => setSelectedHotelId(Number(event.target.value))}
                                    className="rate-adjustments-select"
                                >
                                    {hotels.map((hotel) => (
                                        <option key={hotel.id} value={hotel.id}>
                                            {hotel.name}
                                        </option>
                                    ))}
                                </select>
                            </label>

                            <label className="rate-adjustments-label">
                                Room Type
                                <select
                                    value={selectedRoomTypeId ?? ''}
                                    onChange={(event) => setSelectedRoomTypeId(Number(event.target.value))}
                                    className="rate-adjustments-select"
                                    disabled={loadingRoomTypes || roomTypes.length === 0}
                                >
                                    {roomTypes.length === 0 ? (
                                        <option value="">No room types</option>
                                    ) : (
                                        roomTypes.map((room) => (
                                            <option key={room.id} value={room.id}>
                                                {room.name}
                                            </option>
                                        ))
                                    )}
                                </select>
                            </label>

                            <Input
                                label="Adjustment Amount"
                                type="number"
                                step="0.01"
                                value={amount}
                                onChange={(event) => setAmount(event.target.value)}
                                placeholder="e.g., 10.00 or -5.00"
                                required
                                fullWidth
                            />

                            <Input
                                label="Effective Date"
                                type="date"
                                value={effectiveDate}
                                onChange={(event) => setEffectiveDate(event.target.value)}
                                required
                                fullWidth
                            />

                            <Input
                                label="Reason"
                                type="text"
                                value={reason}
                                onChange={(event) => setReason(event.target.value)}
                                placeholder="Reason for adjustment"
                                required
                                fullWidth
                            />

                            {formError && <div className="rate-adjustments-error">{formError}</div>}

                            <Button type="submit" variant="primary" loading={submitting}>
                                Save Adjustment
                            </Button>
                        </form>
                    </Card>

                    <Card>
                        <h2 className="rate-adjustments-section-title">
                            History {selectedRoomType ? `for ${selectedRoomType.name}` : ''}
                        </h2>
                        {loadingRoomTypes || loadingAdjustments ? (
                            <Loader text="Loading adjustments..." />
                        ) : adjustments.length === 0 ? (
                            <div className="rate-adjustments-empty">
                                No adjustments recorded for {selectedHotel?.name ?? 'this hotel'}.
                            </div>
                        ) : (
                            <ul className="rate-adjustments-list">
                                {adjustments.map((adjustment) => (
                                    <li key={adjustment.id} className="rate-adjustments-list__item">
                                        <div className="rate-adjustments-list__row">
                                            <span>{adjustment.effective_date}</span>
                                            <span className="rate-adjustments-list__amount">
                                                {adjustment.adjustment_amount >= 0 ? '+' : ''}
                                                {adjustment.adjustment_amount.toFixed(2)}
                                            </span>
                                        </div>
                                        <p className="rate-adjustments-list__reason">{adjustment.reason}</p>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </Card>
                </div>
            </div>
        </MainLayout>
    );
};
