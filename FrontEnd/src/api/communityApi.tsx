import { customAxios } from '@src/util/auth/customAxios'
import {
  CommentCreateType,
  CommentDeleteDataType,
  CommentListDataType,
  CommentModifyDataType,
  CommunityCreateDataType,
  CommunityModifyDataType,
  ImageUploadPromiseType,
} from '@src/types/CommunityType'

// 커뮤니티 목록 get api
export const fetchCommunityList = async (category: string, lastId: number) => {
  return customAxios
    .get(`/community?category=${category}&lastId=${lastId}`)
    .then(res => res.data)
    .catch(err => console.log(err))
}

// 커뮤니티 상세 get api
export const fetchCommunityDetail = async (communityId: number) => {
  return customAxios
    .get(`/community/${communityId}`)
    .then(res => res.data)
    .catch(err => console.log(err))
}

// 커뮤니티 게시글 생성 post api
export const communityCreate = async (data: CommunityCreateDataType) => {
  return customAxios
    .post(`/community`, data)
    .then(res => res.data)
    .catch(err => console.log(err))
}

// 커뮤니티 게시글 생성 post api
export const imageUpload = async (
  data: FormData,
): Promise<ImageUploadPromiseType> => {
  return customAxios
    .post(`/firebase/upload`, data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    .then(res => res.data)
    .catch(err => console.log(err))
}

// 커뮤니티 게시글 수정 patch api
export const communityModify = async (data: CommunityModifyDataType) => {
  return customAxios
    .patch(`/community/${data.communityId}`, data.data)
    .then(res => res.data)
    .catch(err => console.log(err))
}

// 게시글 삭제 delete api
export const articleDelete = async (communityId: number) => {
  return customAxios
    .delete(`/community/${communityId}`)
    .then(res => res.data)
    .catch(err => console.log(err))
}

// 커뮤니티 댓글 생성 post api
export const commentCreate = async (
  commentCreateData: CommentCreateType,
): Promise<CommentListDataType> => {
  return customAxios
    .post(
      `/community/${commentCreateData.communityId}/comment`,
      commentCreateData.data,
    )
    .then(res => res.data)
    .catch(err => console.log(err))
}
// 커뮤니티 댓글 조회 get api
export const fetchCommentList = async (communityId: number) => {
  return customAxios
    .get(`/community/${communityId}/comment`)
    .then(res => res.data)
    .catch(err => console.log(err))
}
// 커뮤니티 댓글 조회 get api
export const commentModify = async (
  commentModifyData: CommentModifyDataType,
) => {
  return customAxios
    .patch(
      `/community/${commentModifyData.communityId}/comment/${commentModifyData.commentId}`,
      commentModifyData.data,
    )
    .then(res => res.data)
    .catch(err => console.log(err))
}

// 댓글 삭제 delete api
export const commentDelete = async (
  commentDeleteData: CommentDeleteDataType,
) => {
  return customAxios
    .delete(
      `/community/${commentDeleteData.communityId}/comment/${commentDeleteData.commentId}`,
    )
    .then(res => res.data)
    .catch(err => console.log(err))
}

// 인기 커뮤니티 목록 조회 get api
export const fetchPopularArticle = async () => {
  return customAxios
    .get(`/community/popular`)
    .then(res => res.data)
    .catch(err => console.log(err))
}
