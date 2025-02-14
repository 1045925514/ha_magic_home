# -*- coding: utf-8 -*-
"""
The Ha Magic Home integration iot/device_class File.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class Attribute:
    name: str
    scale: str
    timestampOfSample: int
    uncertaintyInMilliseconds: int
    value: int
    legalValue: str


@dataclass
class AdditionalApplianceDetails:
    aeskeyToken: str
    blecategory: str
    bledevtype: str
    bledevversion: str
    bletoken: str
    capDynamic: str
    devname: str
    did: str
    familyid: str
    familyname: str
    gatewayblesupport: str
    isPreDefineCategory: Optional[None]
    loopSceneGatewaydid: str
    moduleid: str
    moduletype: str
    newintent: str
    onlycommand: str
    orifriendlyName: str
    pid: str
    range: str
    room: str
    sdid: str
    shortaddr: str
    spid: str
    tokenlist: str
    userid: str
    version: str
    vtdid: str


@dataclass
class Appliance:
    actions: List[str]
    additionalApplianceDetails: AdditionalApplianceDetails
    applianceId: str
    applianceTypes: List[str]
    friendlyDescription: str
    friendlyName: str
    isReachable: bool
    manufacturerName: str
    modelName: str
    version: str
    attributes: List[Attribute]


@dataclass
class XdHeaderStu:
    name: str
    namespace: str
    messageid: str
    payloadversion: str


@dataclass
class XdBody:
    header: XdHeaderStu
    payload: Dict[str, Any]


import json
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class Supported(BaseModel):
    name: Optional[str] = None
    range: Optional[Dict[str, Any]] = None
    enums: Optional[List[str]] = None


class Properties(BaseModel):
    supported: Optional[List[Supported]] = None
    proactivelyReported: Optional[bool] = None
    retrievable: Optional[bool] = None


class Actions(BaseModel):
    supported: Optional[List[Supported]] = None


class Capability(BaseModel):
    type: Optional[str] = None
    interface: Optional[str] = None
    version: Optional[str] = None
    properties: Optional[Properties] = None
    actions: Optional[Actions] = None
    supportsDeactivation: Optional[bool] = None
    proactivelyReported: Optional[bool] = None


class Cookie(BaseModel):
    Pid: Optional[str] = None
    aeskeyToken: Optional[str] = None
    bletoken: Optional[str] = None
    did: Optional[str] = None
    openmqtt: Optional[str] = None
    room: Optional[str] = None
    sceneflag: Optional[str] = None
    sdid: Optional[str] = None
    tokenlist: Optional[str] = None
    vtdid: Optional[str] = None
    pid: Optional[str] = None
    spid: Optional[str] = None
    userid: Optional[str] = None
    devname: Optional[str] = None
    moduleid: Optional[str] = None
    moduletype: Optional[str] = None
    familyid: Optional[str] = None
    familyname: Optional[str] = None
    version: Optional[str] = None
    isPreDefineCategory: Optional[bool] = None
    range: Optional[str] = None
    shortaddr: Optional[str] = None
    blecategory: Optional[str] = None
    bledevtype: Optional[str] = None
    capDynamic: Optional[str] = None
    onlycommand: Optional[str] = None
    bledevversion: Optional[str] = None
    orifriendlyName: Optional[str] = None
    gatewayblesupport: Optional[str] = None
    loopSceneGatewaydid: Optional[str] = None


class Scene(BaseModel):
    sceneId: Optional[str] = None
    friendlyName: Optional[str] = None
    icon: Optional[str] = None
    manufacturerName: Optional[str] = None
    description: Optional[str] = None
    displayCategories: Optional[List[str]] = None
    cookie: Optional[Cookie] = None
    capabilities: Optional[List[Capability]] = None
    floor: Optional[str] = None
    roomName: Optional[str] = None
    ignoreflag: Optional[bool] = None


class Endpoint(BaseModel):
    endpointId: Optional[str] = None
    parentId: Optional[str] = None
    friendlyName: Optional[str] = None
    description: Optional[str] = None
    manufacturerName: Optional[str] = None
    icon: Optional[str] = None
    brand: Optional[str] = None
    floor: Optional[str] = None
    roomName: Optional[str] = None
    displayCategories: Optional[List[str]] = None
    displayCategories_v2: Optional[str] = None
    cookie: Optional[Cookie] = None
    isReachable: Optional[bool] = None
    capabilities: Optional[List[Capability]] = None
    additional: Optional[Any] = None
    sn: Optional[str] = None
    fwversion: Optional[str] = None
    model: Optional[str] = None


class Scope(BaseModel):
    type: Optional[str] = None
    token: Optional[str] = None
    mtag: Optional[str] = None
    spacemtag: Optional[str] = None
    endpointid: Optional[str] = None


class EndpointScope(BaseModel):
    scope: Optional[Scope] = None
    endpointId: Optional[str] = None


class Header(BaseModel):
    namespace: Optional[str] = None
    name: Optional[str] = None
    interfaceVersion: Optional[str] = None
    messageId: Optional[str] = None


class Payload(BaseModel):
    status: Optional[int] = None
    type: Optional[str] = None


class Event(BaseModel):
    header: Optional[Header] = None
    payload: Optional[Payload] = None
    scenes: Optional[List[Scene]] = None
    endpoints: Optional[List[Endpoint]] = None
    hiddenEndPoints: Optional[Any] = None
    eventEndPoints: Optional[Any] = None
    endpoint: Optional[EndpointScope] = None


class Context(BaseModel):
    properties: Optional[Any] = None


class Discovery(BaseModel):
    context: Optional[Context] = None
    event: Optional[Event] = None


class Scope(BaseModel):
    type: str = ""
    token: str = ""


class ControlEndpoint(BaseModel):
    scope: Scope = Scope()
    endpointId: str = ""
    cookie: Dict[str, Any] = {}


class ControlHeader(BaseModel):
    namespace: str = ""
    name: str = ""
    interfaceVersion: str = ""
    messageId: str = ""


class Directive(BaseModel):
    header: ControlHeader = ControlHeader()
    endpoint: ControlEndpoint = ControlEndpoint()
    payload: Dict[str, Any] = {}


class ControlModel(BaseModel):
    directive: Directive = Directive()


class Value(BaseModel):
    scale: str
    scaleName: str
    attributeName: str
    value: Any
    valueName: str


class ResProperty(BaseModel):
    namespace: str
    name: str
    value: Value
    extend: str
    timeOfSample: str


class Context(BaseModel):
    properties: List[ResProperty]


class ResEvent(BaseModel):
    payload: Payload


class ResponseModel(BaseModel):
    context: Context
    event: ResEvent


class ControlResponse(BaseModel):
    event: ResEvent
