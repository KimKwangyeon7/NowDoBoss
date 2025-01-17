package com.ssafy.backend.domain.chat.dto.response;

import com.ssafy.backend.domain.community.entity.enums.Category;

public record ChatRoomListResponse(
        Long chatRoomId,
        Category category,
        String name,
        int memberCount,
        int limit
) {
}
