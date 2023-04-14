package trash_project.demo.member.dto;

import lombok.*;
import trash_project.demo.member.entity.CctvEntity;
import trash_project.demo.member.entity.MemberEntity;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class CctvDTO {
    private Long no;
    private String cctvAddressStreet;
    private String cctvAddressDetail;
    private String cctvAlias;
    private MemberEntity memberEntity;

    public static CctvDTO toCctvDTO(CctvEntity cctvEntity) {
        CctvDTO cctvDTO = new CctvDTO();
        cctvDTO.setNo(cctvEntity.getNo());
        cctvDTO.setCctvAddressStreet(cctvEntity.getCctvAddressStreet());
        cctvDTO.setCctvAddressDetail(cctvEntity.getCctvAddressDetail());
        cctvDTO.setCctvAlias(cctvEntity.getCctvAlias());
        cctvDTO.setMemberEntity(cctvEntity.getMemberEntity());

        return cctvDTO;
    }
}
