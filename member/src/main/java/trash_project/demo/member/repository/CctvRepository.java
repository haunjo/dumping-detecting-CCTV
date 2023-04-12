package trash_project.demo.member.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import trash_project.demo.member.entity.CctvEntity;
import trash_project.demo.member.entity.MemberEntity;

import java.util.List;

public interface CctvRepository extends JpaRepository<CctvEntity, String> {
    List<CctvEntity> findByMemberEntity(MemberEntity memberEntity);
}
