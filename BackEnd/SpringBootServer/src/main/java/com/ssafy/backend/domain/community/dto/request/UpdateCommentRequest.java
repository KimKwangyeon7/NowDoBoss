package com.ssafy.backend.domain.community.dto.request;

import jakarta.validation.constraints.NotBlank;

public record UpdateCommentRequest(
        @NotBlank(message = "내용을 입력해주세요")
        String content
) {
}
