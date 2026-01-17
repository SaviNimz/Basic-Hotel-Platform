import { apiClient } from './client';
import type {
    RoomType,
    RoomTypeCreate,
    RateAdjustment,
    RateAdjustmentCreate,
    EffectiveRateResponse
} from './types';


export const createRoomType = async (roomType: RoomTypeCreate): Promise<RoomType> => {
    const response = await apiClient.post<RoomType>('/room-types/', roomType);
    return response.data;
};


export const createRateAdjustment = async (
    adjustment: RateAdjustmentCreate
): Promise<RateAdjustment> => {
    const response = await apiClient.post<RateAdjustment>('/rate-adjustments/', adjustment);
    return response.data;
};


export const getEffectiveRate = async (
    roomTypeId: number,
    date?: string
): Promise<EffectiveRateResponse> => {
    const params = date ? { date_str: date } : {};
    const response = await apiClient.get<EffectiveRateResponse>(
        `/room-types/${roomTypeId}/effective-rate`,
        { params }
    );
    return response.data;
};
