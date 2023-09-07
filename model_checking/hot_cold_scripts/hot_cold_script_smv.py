from pynusmv.model import *

class threeC(Module):
    event = Identifier("event")
    ARGS = [event]
    state = Var(Range(1, 4))
    HOT_req = Var(Boolean())
    COLD_req = Var(Boolean())
    HOT_blocked = Var(Boolean())
    COLD_blocked = Var(Boolean())
    INIT = [state == 1]
    ASSIGN = {"HOT_req": "FALSE",
              "HOT_blocked": "FALSE",
              "COLD_blocked": "FALSE",
              "next(state)": Case(((state == 4, 4),
                                   (event.next() == "COLD", state + 1),
                                   (Trueexp(), state))),
              "COLD_req": Case(((state == 1, Trueexp()),
                                (state == 2, Trueexp()),
                                (state == 3, Trueexp()),
                                (Trueexp(), Falseexp()),))
              }

class threeH(Module):
    event = Identifier("event")
    ARGS = [event]
    state = Var(Range(1, 4))
    HOT_req = Var(Boolean())
    COLD_req = Var(Boolean())
    HOT_blocked = Var(Boolean())
    COLD_blocked = Var(Boolean())
    INIT = [state == 1]
    ASSIGN = {"COLD_req": "FALSE",
              "HOT_blocked": "FALSE",
              "COLD_blocked": "FALSE",
              "next(state)" : Case(((state == 4, 4),
                                   (event.next() == "HOT", state + 1),
                                   (Trueexp(), state))),
              "HOT_req": Case(((state == 1, Trueexp()),
                                (state == 2, Trueexp()),
                                (state == 3, Trueexp()),
                                (Trueexp(), Falseexp()),))
              }

class control(Module):
    event = Identifier("event")
    ARGS = [event]
    state = Var(Range(1, 2))
    HOT_blocked = Var(Boolean())
    COLD_blocked = Var(Boolean())
    INIT = [state == 1]
    ASSIGN = {"COLD_blocked": "FALSE",
              "next(state)": Case(((And(state == 1, event.next() == "HOT"), 2),
                                  (And(state == 2, event.next() == "COLD"), 1),
                                  (Trueexp(), state))),
              "HOT_blocked": Case(((state == 2, Trueexp()),
                               (Trueexp(), Falseexp()),))
              }

class main(Module):
    event = Var(Scalar(("START", "HOT", "COLD", "DONE", "STOPPED")))
    bt1 = Var(threeH(event))
    bt2 = Var(threeC(event))
    bt3 = Var(control(event))
    INIT = [event == "START"]
    DEFINE = {
        "HOT_req": Or(bt1.HOT_req, bt2.HOT_req),
        "COLD_req": Or(bt1.COLD_req, bt2.COLD_req),
        "HOT_blocked": Or(bt1.HOT_blocked, Or(bt2.HOT_blocked, bt3.HOT_blocked)),
        "COLD_blocked": Or(bt1.COLD_blocked, Or(bt2.COLD_blocked, bt3.COLD_blocked))
    }
    ASSIGN = {
        "next(event)" : Case(((event == "DONE", "DONE"),
                              (event == "STOPPED", "STOPPED"),
                              (And("HOT_req", And(Not("HOT_blocked"), Or(Not("COLD_req"), "COLD_blocked"))), "HOT"),
                              (And("COLD_req", And(Not("COLD_blocked"), Or(Not("HOT_req"), "HOT_blocked"))), "COLD"),
                              (And("HOT_req", And(Not("HOT_blocked"), And("COLD_req", Not("COLD_blocked")))), "{HOT, COLD}"),
                              (And(bt1.state == 4, bt2.state == 4), "DONE"),
                              (Trueexp(), "STOPPED")))
    }


