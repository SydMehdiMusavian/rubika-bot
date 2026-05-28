from Rubika.Create_Update import Main_Update, Message
import inspect
import Rubika.Filter as Filter
from Rubika.FinitState import StateInjection , state
from Rubika.Config_Logger import bot_logger
class router:
    def __init__(self):
        self.message_handler = []
    
    async def runingMethod(self, method, MessageObj: Main_Update = None, FSM: StateInjection = None):
        sig = inspect.signature(method)

        available = {
            'message': MessageObj, 'msg': MessageObj, 'Message': MessageObj,
            'state': FSM, 'fsm': FSM, 'Fsm': FSM, 'State': FSM
        }
        
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param.annotation == Message:
                kwargs[param_name] = MessageObj
            elif param.annotation == StateInjection:
                kwargs[param_name] = FSM
            elif param_name in available:
                kwargs[param_name] = available[param_name]
        
        try:
            bound = sig.bind_partial(**kwargs)
            bound.apply_defaults()
            await method(*bound.args, **bound.kwargs)
        except TypeError as e:
            bot_logger.error(f"❌ خطا در فراخوانی {method}: {e}")

    async def __call__(self, Update:Main_Update):
        for routerTupel in self.message_handler:
            if isinstance(routerTupel[0],Filter.Text):
                if routerTupel[0].checker(update_object=Update):
                    await self.runingMethod(method=routerTupel[1],MessageObj=Update,FSM=Update.FsmContext)
                    return True
            elif isinstance(routerTupel[0],Filter.ChatType):
                if routerTupel[0].checker(update_object=Update):
                    await self.runingMethod(method=routerTupel[1],MessageObj=Update,FSM=Update.FsmContext)
                    return True
            elif isinstance(routerTupel[0],Filter.Combine):
                if routerTupel[0].checker(update_object=Update):
                    await self.runingMethod(method=routerTupel[1],MessageObj=Update,FSM=Update.FsmContext)
                    return True
            elif isinstance(routerTupel[0],Filter.Reg):
                if routerTupel[0].checker(update_object=Update):
                    await self.runingMethod(method=routerTupel[1],MessageObj=Update,FSM=Update.FsmContext)
                    return True
            elif isinstance(routerTupel[0],Filter.Documents):
                if routerTupel[0].checker(update_object=Update):
                    await self.runingMethod(method=routerTupel[1],MessageObj=Update,FSM=Update.FsmContext)
                    return True
            elif isinstance(routerTupel[0],Filter.GeneralFilter):
                if routerTupel[0].checker(update_object=Update):
                    await self.runingMethod(method=routerTupel[1],MessageObj=Update,FSM=Update.FsmContext)
                    return True
            elif isinstance(routerTupel[0],Filter.StateFilter):
                if routerTupel[0].checker(update_object=Update):
                    await self.runingMethod(method=routerTupel[1],MessageObj=Update,FSM=Update.FsmContext)
                    return True
            else :
                return False

    def message(self,*arguments):
        def wrapper(fn):
            for arg in arguments:
                if isinstance(arg,str):
                    self.message_handler.append((Filter.Text(arg),fn))
                elif isinstance(arg,state):
                    self.message_handler.append((Filter.StateFilter(arg),fn))
                else:
                    self.message_handler.append((arg,fn))
            return fn
        return wrapper

