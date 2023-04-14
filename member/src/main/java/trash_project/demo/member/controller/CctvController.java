package trash_project.demo.member.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.HttpMediaTypeException;
import org.springframework.web.bind.annotation.*;
import trash_project.demo.member.dto.CctvDTO;
import trash_project.demo.member.entity.MemberEntity;
import trash_project.demo.member.repository.MemberRepository;
import trash_project.demo.member.service.CctvService;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import java.util.List;


@Controller
@RequestMapping("/cctv")
@RequiredArgsConstructor
public class CctvController {
    // 생성자 주입
    private final CctvService cctvService;
    private final MemberRepository memberRepository;

    // cctv 등록 페이지 출력 요청
    @GetMapping("/register")
    public String registerForm() {
        return "cctv_register";
    }

    @PostMapping("/register")
    public String register(@ModelAttribute CctvDTO cctvDTO, HttpServletRequest request) {
        HttpSession httpSession = request.getSession();
        String loginId = (String) httpSession.getAttribute("Id");

        cctvService.register(cctvDTO, loginId);

        return "main";
    }

    @GetMapping("/list")
    public String myCctv(Model model, HttpServletRequest request) {
        HttpSession httpSession = request.getSession();
        String loginId = (String) httpSession.getAttribute("Id");
        MemberEntity memberEntity = memberRepository.findByMemberId(loginId).get();

        List<CctvDTO> cctvDTOList = cctvService.findByMemberEntity(memberEntity);
        // 어떠한 html로 가져갈 데이터가 있다면 model 사용
        model.addAttribute("cctvList", cctvDTOList);
        return "cctv_list";
    }

    @GetMapping("/{no}")
    public String checkCctv(@PathVariable Long no, Model model) {
        model.addAttribute("no", no);
        return "cctv_check";
    }

    @GetMapping("/modify/{no}")
    public String modifyCctv(@PathVariable Long no, Model model){
        CctvDTO cctvDTO = cctvService.updateForm(no);
        model.addAttribute("updateCctv", cctvDTO);
        return "cctv_update";
    }

    @PostMapping("/modify/{no}")
    public String update(@ModelAttribute CctvDTO cctvDTO, HttpSession session) {
        String loginId = (String) session.getAttribute("Id");
        cctvService.update(cctvDTO, loginId);
        return "redirect:/cctv/list";
    }

    @GetMapping("/delete/{no}")
    public String deleteCctv(@PathVariable Long no) {
        cctvService.deleteCctv(no);
        return "redirect:/cctv/list";
    }
}
