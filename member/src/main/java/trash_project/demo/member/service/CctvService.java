package trash_project.demo.member.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import trash_project.demo.member.dto.CctvDTO;
import trash_project.demo.member.entity.CctvEntity;
import trash_project.demo.member.entity.MemberEntity;
import trash_project.demo.member.repository.CctvRepository;
import trash_project.demo.member.repository.MemberRepository;

import java.lang.reflect.Member;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class CctvService {

    private final CctvRepository cctvRepository;
    private final MemberRepository memberRepository;

    public void register(CctvDTO cctvDTO, String loginId) {
        CctvEntity cctvEntity = CctvEntity.toCctvEntity(cctvDTO);
        MemberEntity memberEntity = memberRepository.findByMemberId(loginId).get();
        cctvEntity.setMemberEntity(memberEntity);
//        System.out.println(cctvEntity);
        cctvRepository.save(cctvEntity);
//        System.out.println(cctvEntity.getMemberEntity());
//        System.out.println(cctvEntity.getMemberEntity().getMemberName());
    }

    public List<CctvDTO> findByMemberEntity(MemberEntity memberEntity) { //id는 로그인한 memberId
        List<CctvEntity> cctvEntityList = cctvRepository.findByMemberEntity(memberEntity);
        List<CctvDTO> cctvDTOList = new ArrayList<>();
        for (CctvEntity cctvEntity : cctvEntityList) {
            cctvDTOList.add(CctvDTO.toCctvDTO(cctvEntity));
        }
        return cctvDTOList;
    }

    public void deleteCctv(Long no) {
//        cctvRepository.deleteByNo(no);
        cctvRepository.deleteById(no);
    }
}