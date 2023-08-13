from pydantic import BaseModel


class CustomerModel(BaseModel):
    id: str
    sim_id: int
    name: str
    payment_type: str
    exit_type: int
    reputation: int
    item_list: dict
    start_time: str
    end_time: str
