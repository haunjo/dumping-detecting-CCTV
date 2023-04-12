package trash_project.demo.member.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.transaction.annotation.Transactional;
import trash_project.demo.member.entity.CctvEntity;
import trash_project.demo.member.entity.MemberEntity;

import java.util.List;

public interface CctvRepository extends JpaRepository<CctvEntity, Long> {
    List<CctvEntity> findByMemberEntity(MemberEntity memberEntity);
//    @Transactional
//    @Modifying
//    @Query("delete from CctvEntity m where m.no= :no")
//    public void deleteByNo(@Param("no") Long no);

}
