package trash_project.demo.member.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import trash_project.demo.member.dto.MemberDTO;
import trash_project.demo.member.service.MemberService;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

@Controller
@RequestMapping("/member")
@RequiredArgsConstructor
public class MemberController {
    // 생성자 주입
    private final MemberService memberService;

    // 회원가입 페이지 출력 요청
    @GetMapping("/save")
    public String saveForm() {
        return "save";
    }

    @PostMapping("/save")
    public String save(@ModelAttribute MemberDTO memberDTO) {
        memberService.save(memberDTO);
        return "index";
    }

    @GetMapping("/login")
    public String loginForm() {
        return "login";
    }

    @PostMapping("/login")
    public String login(@ModelAttribute MemberDTO memberDTO, HttpServletRequest request) {
        MemberDTO loginResult = memberService.login(memberDTO);
//        System.out.println(memberDTO);
//        System.out.println(session.getAttribute("Id"));

        if (loginResult != null) {
            // login 성공
//            session.setAttribute("loginNo", loginResult.getNo());
            HttpSession session = request.getSession();
            session.setAttribute("Id", loginResult.getMemberId());
            return "main";
        } else {
            // login 실패
            return "login";
        }
    }

    @GetMapping("/update")
    public String updateForm(HttpSession session, Model model) {
        String myId = (String) session.getAttribute("Id");
//        System.out.println(myId);
        MemberDTO memberDTO = memberService.updateForm(myId);
//        System.out.println("--" + memberDTO);
        model.addAttribute("updateMember", memberDTO);
        return "member_update";
    }

    @PostMapping("/update")
    public String update(@ModelAttribute MemberDTO memberDTO) {
//        System.out.println("++" + memberDTO);
        memberService.update(memberDTO);
        return "redirect:/member/login";
    }

    @GetMapping("/delete/{no}")
    public String deleteById(@PathVariable Long no) {
        memberService.deleteById(no);
        return "redirect:/";
    }

    @GetMapping("/logout")
    public String logout(HttpSession session){
        session.invalidate();
        return "redirect:/";
    }
}

