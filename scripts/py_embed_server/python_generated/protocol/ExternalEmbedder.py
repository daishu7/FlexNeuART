#
# Autogenerated by Thrift Compiler (0.13.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys
import logging
from .ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
all_structs = []


class Iface(object):
    def embedDocuments(self, docs):
        """
        Parameters:
         - docs

        """
        pass

    def embedQuery(self, query):
        """
        Parameters:
         - query

        """
        pass


class Client(Iface):
    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    def embedDocuments(self, docs):
        """
        Parameters:
         - docs

        """
        self.send_embedDocuments(docs)
        return self.recv_embedDocuments()

    def send_embedDocuments(self, docs):
        self._oprot.writeMessageBegin('embedDocuments', TMessageType.CALL, self._seqid)
        args = embedDocuments_args()
        args.docs = docs
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_embedDocuments(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = embedDocuments_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        raise TApplicationException(TApplicationException.MISSING_RESULT, "embedDocuments failed: unknown result")

    def embedQuery(self, query):
        """
        Parameters:
         - query

        """
        self.send_embedQuery(query)
        return self.recv_embedQuery()

    def send_embedQuery(self, query):
        self._oprot.writeMessageBegin('embedQuery', TMessageType.CALL, self._seqid)
        args = embedQuery_args()
        args.query = query
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_embedQuery(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = embedQuery_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.err is not None:
            raise result.err
        raise TApplicationException(TApplicationException.MISSING_RESULT, "embedQuery failed: unknown result")


class Processor(Iface, TProcessor):
    def __init__(self, handler):
        self._handler = handler
        self._processMap = {}
        self._processMap["embedDocuments"] = Processor.process_embedDocuments
        self._processMap["embedQuery"] = Processor.process_embedQuery
        self._on_message_begin = None

    def on_message_begin(self, func):
        self._on_message_begin = func

    def process(self, iprot, oprot):
        (name, type, seqid) = iprot.readMessageBegin()
        if self._on_message_begin:
            self._on_message_begin(name, type, seqid)
        if name not in self._processMap:
            iprot.skip(TType.STRUCT)
            iprot.readMessageEnd()
            x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
            oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
            x.write(oprot)
            oprot.writeMessageEnd()
            oprot.trans.flush()
            return
        else:
            self._processMap[name](self, seqid, iprot, oprot)
        return True

    def process_embedDocuments(self, seqid, iprot, oprot):
        args = embedDocuments_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = embedDocuments_result()
        try:
            result.success = self._handler.embedDocuments(args.docs)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TApplicationException as ex:
            logging.exception('TApplication exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = ex
        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
        oprot.writeMessageBegin("embedDocuments", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_embedQuery(self, seqid, iprot, oprot):
        args = embedQuery_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = embedQuery_result()
        try:
            result.success = self._handler.embedQuery(args.query)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except EmbeddingException as err:
            msg_type = TMessageType.REPLY
            result.err = err
        except TApplicationException as ex:
            logging.exception('TApplication exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = ex
        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
        oprot.writeMessageBegin("embedQuery", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

# HELPER FUNCTIONS AND STRUCTURES


class embedDocuments_args(object):
    """
    Attributes:
     - docs

    """


    def __init__(self, docs=None,):
        self.docs = docs

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.LIST:
                    self.docs = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in range(_size0):
                        _elem5 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        self.docs.append(_elem5)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('embedDocuments_args')
        if self.docs is not None:
            oprot.writeFieldBegin('docs', TType.LIST, 1)
            oprot.writeListBegin(TType.STRING, len(self.docs))
            for iter6 in self.docs:
                oprot.writeString(iter6.encode('utf-8') if sys.version_info[0] == 2 else iter6)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.docs is None:
            raise TProtocolException(message='Required field docs is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(embedDocuments_args)
embedDocuments_args.thrift_spec = (
    None,  # 0
    (1, TType.LIST, 'docs', (TType.STRING, 'UTF8', False), None, ),  # 1
)


class embedDocuments_result(object):
    """
    Attributes:
     - success

    """


    def __init__(self, success=None,):
        self.success = success

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    (_etype10, _size7) = iprot.readListBegin()
                    for _i11 in range(_size7):
                        _elem12 = []
                        (_etype16, _size13) = iprot.readListBegin()
                        for _i17 in range(_size13):
                            _elem18 = iprot.readDouble()
                            _elem12.append(_elem18)
                        iprot.readListEnd()
                        self.success.append(_elem12)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('embedDocuments_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.LIST, len(self.success))
            for iter19 in self.success:
                oprot.writeListBegin(TType.DOUBLE, len(iter19))
                for iter20 in iter19:
                    oprot.writeDouble(iter20)
                oprot.writeListEnd()
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(embedDocuments_result)
embedDocuments_result.thrift_spec = (
    (0, TType.LIST, 'success', (TType.LIST, (TType.DOUBLE, None, False), False), None, ),  # 0
)


class embedQuery_args(object):
    """
    Attributes:
     - query

    """


    def __init__(self, query=None,):
        self.query = query

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.query = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('embedQuery_args')
        if self.query is not None:
            oprot.writeFieldBegin('query', TType.STRING, 1)
            oprot.writeString(self.query.encode('utf-8') if sys.version_info[0] == 2 else self.query)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.query is None:
            raise TProtocolException(message='Required field query is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(embedQuery_args)
embedQuery_args.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'query', 'UTF8', None, ),  # 1
)


class embedQuery_result(object):
    """
    Attributes:
     - success
     - err

    """


    def __init__(self, success=None, err=None,):
        self.success = success
        self.err = err

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    (_etype24, _size21) = iprot.readListBegin()
                    for _i25 in range(_size21):
                        _elem26 = iprot.readDouble()
                        self.success.append(_elem26)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.err = EmbeddingException()
                    self.err.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('embedQuery_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.DOUBLE, len(self.success))
            for iter27 in self.success:
                oprot.writeDouble(iter27)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.err is not None:
            oprot.writeFieldBegin('err', TType.STRUCT, 1)
            self.err.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(embedQuery_result)
embedQuery_result.thrift_spec = (
    (0, TType.LIST, 'success', (TType.DOUBLE, None, False), None, ),  # 0
    (1, TType.STRUCT, 'err', [EmbeddingException, None], None, ),  # 1
)
fix_spec(all_structs)
del all_structs

