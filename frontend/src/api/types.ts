// Hotel Types
export interface HotelBase {
  name: string;
  location: string;
  is_active: boolean;
}


export interface HotelCreate extends HotelBase {}


export interface HotelUpdate {
  name?: string;
  location?: string;
  is_active?: boolean;
}


export interface Hotel extends HotelBase {
  id: number;
}

// Room Type
export interface RoomTypeBase {
  name: string;
  base_rate: number;
  hotel_id: number;
}


export interface RoomTypeCreate extends RoomTypeBase {}


export interface RoomTypeUpdate {
  name?: string;
  base_rate?: number;
  hotel_id?: number;
}


export interface RoomType extends RoomTypeBase {
  id: number;
}

// Rate Adjustment
export interface RateAdjustmentBase {
  room_type_id: number;
  adjustment_amount: number;
  effective_date: string; // ISO date string
  reason: string;
}


export interface RateAdjustmentCreate extends RateAdjustmentBase {}


export interface RateAdjustment extends RateAdjustmentBase {
  id: number;
}

// Effective Rate Response
export interface EffectiveRateResponse {
  room_type_id: number;
  base_rate: number;
  effective_rate: number;
  adjustment_applied: number;
  effective_date: string;
}

// Auth Types
export interface UserLogin {
  username: string;
  password: string;
}


export interface Token {
  access_token: string;
  token_type: string;
}

// API Error Response
export interface ApiError {
  detail: string | { loc: string[]; msg: string; type: string }[];
}
