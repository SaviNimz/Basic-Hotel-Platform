# Backend API Documentation

This document describes every API endpoint exposed by the Basic Hotel Platform backend.

## Base URL

All endpoints below are served under the base URL configured for the backend (for example, `http://localhost:8000`).

## Authentication

Most endpoints require a valid Bearer token. Obtain a token via the login endpoint and pass it in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

### POST `/auth/token`

**Description:** Authenticate a user and return an access token.

**Auth required:** No.

**Request (form data):**
- `username` (string, required)
- `password` (string, required)

**Response:**
- `access_token` (string)
- `token_type` (string, typically `bearer`)

**Errors:**
- `401 Unauthorized` if credentials are invalid.

## Users

> All `/users` endpoints require authentication.

### GET `/users/me`

**Description:** Return the current authenticated user’s ID and username.

**Auth required:** Yes.

**Response:**
- `id` (integer)
- `username` (string)

### POST `/users/`

**Description:** Create a new user.

**Auth required:** Yes.

**Request body:** `UserCreate`
- `username` (string, required)
- `password` (string, required)

**Response:** `User`
- `id` (integer)
- `username` (string)

**Errors:**
- `400 Bad Request` if the username is already registered.

### GET `/users/`

**Description:** List users.

**Auth required:** Yes.

**Query parameters:**
- `skip` (integer, default `0`)
- `limit` (integer, default `100`)

**Response:** Array of `User` objects.

### GET `/users/{user_id}`

**Description:** Get a user by ID.

**Auth required:** Yes.

**Path parameters:**
- `user_id` (integer, required)

**Response:** `User`

**Errors:**
- `404 Not Found` if the user does not exist.

### PUT `/users/{user_id}`

**Description:** Update a user by ID.

**Auth required:** Yes.

**Path parameters:**
- `user_id` (integer, required)

**Request body:** `UserUpdate`
- `username` (string, optional)
- `password` (string, optional)

**Response:** `User`

**Errors:**
- `404 Not Found` if the user does not exist.
- `400 Bad Request` if the username is already registered by a different user.

### DELETE `/users/{user_id}`

**Description:** Delete a user by ID.

**Auth required:** Yes.

**Path parameters:**
- `user_id` (integer, required)

**Response:** `User` (the deleted record).

**Errors:**
- `404 Not Found` if the user does not exist.

## Hotels

> All `/hotels` endpoints require authentication.

### POST `/hotels/`

**Description:** Create a hotel.

**Auth required:** Yes.

**Request body:** `HotelCreate`
- `name` (string, required)
- `location` (string, required)
- `is_active` (boolean, optional, default `true`)

**Response:** `Hotel`
- `id` (integer)
- `name` (string)
- `location` (string)
- `is_active` (boolean)

### GET `/hotels/`

**Description:** List hotels.

**Auth required:** Yes.

**Query parameters:**
- `skip` (integer, default `0`)
- `limit` (integer, default `100`)

**Response:** Array of `Hotel` objects.

### GET `/hotels/{hotel_id}`

**Description:** Get a hotel by ID.

**Auth required:** Yes.

**Path parameters:**
- `hotel_id` (integer, required)

**Response:** `Hotel`

**Errors:**
- `404 Not Found` if the hotel does not exist.

### PUT `/hotels/{hotel_id}`

**Description:** Update a hotel by ID.

**Auth required:** Yes.

**Path parameters:**
- `hotel_id` (integer, required)

**Request body:** `HotelUpdate`
- `name` (string, optional)
- `location` (string, optional)
- `is_active` (boolean, optional)

**Response:** `Hotel`

**Errors:**
- `404 Not Found` if the hotel does not exist.

### DELETE `/hotels/{hotel_id}`

**Description:** Delete a hotel by ID.

**Auth required:** Yes.

**Path parameters:**
- `hotel_id` (integer, required)

**Response:** `Hotel` (the deleted record).

**Errors:**
- `404 Not Found` if the hotel does not exist.

## Room Types

> All room type endpoints require authentication.

### POST `/room-types/`

**Description:** Create a room type.

**Auth required:** Yes.

**Request body:** `RoomTypeCreate`
- `name` (string, required)
- `base_rate` (number, required)
- `hotel_id` (integer, required)

**Response:** `RoomType`
- `id` (integer)
- `name` (string)
- `base_rate` (number)
- `hotel_id` (integer)

### GET `/hotels/{hotel_id}/room-types/`

**Description:** List room types for a hotel.

**Auth required:** Yes.

**Path parameters:**
- `hotel_id` (integer, required)

**Response:** Array of `RoomType` objects.

### GET `/room-types/{room_type_id}`

**Description:** Get a room type by ID.

**Auth required:** Yes.

**Path parameters:**
- `room_type_id` (integer, required)

**Response:** `RoomType`

**Errors:**
- `404 Not Found` if the room type does not exist.

### PUT `/room-types/{room_type_id}`

**Description:** Update a room type by ID.

**Auth required:** Yes.

**Path parameters:**
- `room_type_id` (integer, required)

**Request body:** `RoomTypeUpdate`
- `name` (string, optional)
- `base_rate` (number, optional)
- `hotel_id` (integer, optional)

**Response:** `RoomType`

**Errors:**
- `404 Not Found` if the room type does not exist.
- `404 Not Found` if a provided `hotel_id` does not exist.

### DELETE `/room-types/{room_type_id}`

**Description:** Delete a room type by ID.

**Auth required:** Yes.

**Path parameters:**
- `room_type_id` (integer, required)

**Response:** `RoomType` (the deleted record).

**Errors:**
- `404 Not Found` if the room type does not exist.

## Rate Adjustments

> All rate adjustment endpoints require authentication.

### POST `/rate-adjustments/`

**Description:** Create a rate adjustment for a room type.

**Auth required:** Yes.

**Request body:** `RateAdjustmentCreate`
- `room_type_id` (integer, required)
- `adjustment_amount` (number, required)
- `effective_date` (string, required, `YYYY-MM-DD`)
- `reason` (string, required)

**Response:** `RateAdjustment`
- `id` (integer)
- `room_type_id` (integer)
- `adjustment_amount` (number)
- `effective_date` (string, `YYYY-MM-DD`)
- `reason` (string)

**Errors:**
- `404 Not Found` if the room type does not exist.

### GET `/rate-adjustments/{adjustment_id}`

**Description:** Get a rate adjustment by ID.

**Auth required:** Yes.

**Path parameters:**
- `adjustment_id` (integer, required)

**Response:** `RateAdjustment`

**Errors:**
- `404 Not Found` if the rate adjustment does not exist.

### GET `/room-types/{room_type_id}/rate-adjustments/`

**Description:** List rate adjustments for a room type.

**Auth required:** Yes.

**Path parameters:**
- `room_type_id` (integer, required)

**Response:** Array of `RateAdjustment` objects.

**Errors:**
- `404 Not Found` if the room type does not exist.

### PUT `/rate-adjustments/{adjustment_id}`

**Description:** Update a rate adjustment by ID.

**Auth required:** Yes.

**Path parameters:**
- `adjustment_id` (integer, required)

**Request body:** `RateAdjustmentUpdate`
- `room_type_id` (integer, optional)
- `adjustment_amount` (number, optional)
- `effective_date` (string, optional, `YYYY-MM-DD`)
- `reason` (string, optional)

**Response:** `RateAdjustment`

**Errors:**
- `404 Not Found` if the rate adjustment does not exist.
- `404 Not Found` if a provided `room_type_id` does not exist.

### DELETE `/rate-adjustments/{adjustment_id}`

**Description:** Delete a rate adjustment by ID.

**Auth required:** Yes.

**Path parameters:**
- `adjustment_id` (integer, required)

**Response:** `RateAdjustment` (the deleted record).

**Errors:**
- `404 Not Found` if the rate adjustment does not exist.

## Effective Rates

> The effective rate endpoint requires authentication.

### GET `/room-types/{room_type_id}/effective-rate`

**Description:** Calculate the effective rate for a room type on a given date.

**Auth required:** Yes.

**Path parameters:**
- `room_type_id` (integer, required)

**Query parameters:**
- `date_str` (string, optional, `YYYY-MM-DD`)

**Response:**
- `room_type_id` (integer)
- `base_rate` (number)
- `effective_rate` (number)
- `adjustment_applied` (number)
- `effective_date` (string, `YYYY-MM-DD`)

**Errors:**
- `404 Not Found` if the room type does not exist.
- `422 Unprocessable Entity` if `date_str` is not a valid ISO date.
