# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import abc
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union
import packaging.version
import pkg_resources

from google import auth  # type: ignore
import google.api_core  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1    # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.bigquery_reservation_v1.types import reservation
from google.cloud.bigquery_reservation_v1.types import reservation as gcbr_reservation
from google.protobuf import empty_pb2 as empty  # type: ignore

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            'google-cloud-bigquery-reservation',
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()

try:
    # google.auth.__version__ was added in 1.26.0
    _GOOGLE_AUTH_VERSION = auth.__version__
except AttributeError:
    try:  # try pkg_resources if it is available
        _GOOGLE_AUTH_VERSION = pkg_resources.get_distribution("google-auth").version
    except pkg_resources.DistributionNotFound:  # pragma: NO COVER
        _GOOGLE_AUTH_VERSION = None

_API_CORE_VERSION = google.api_core.__version__


class ReservationServiceTransport(abc.ABC):
    """Abstract transport class for ReservationService."""

    AUTH_SCOPES = (
        'https://www.googleapis.com/auth/bigquery',
        'https://www.googleapis.com/auth/cloud-platform',
    )

    DEFAULT_HOST: str = 'bigqueryreservation.googleapis.com'
    def __init__(
            self, *,
            host: str = DEFAULT_HOST,
            credentials: credentials.Credentials = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            quota_project_id: Optional[str] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            **kwargs,
            ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ':' not in host:
            host += ':443'
        self._host = host

        scopes_kwargs = self._get_scopes_kwargs(self._host, scopes)

        # Save the scopes.
        self._scopes = scopes or self.AUTH_SCOPES

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs("'credentials_file' and 'credentials' are mutually exclusive")

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                                credentials_file,
                                **scopes_kwargs,
                                quota_project_id=quota_project_id
                            )

        elif credentials is None:
            credentials, _ = auth.default(**scopes_kwargs, quota_project_id=quota_project_id)

        # Save the credentials.
        self._credentials = credentials

    # TODO(busunkim): These two class methods are in the base transport
    # to avoid duplicating code across the transport classes. These functions
    # should be deleted once the minimum required versions of google-api-core
    # and google-auth are increased.

    # TODO: Remove this function once google-auth >= 1.25.0 is required
    @classmethod
    def _get_scopes_kwargs(cls, host: str, scopes: Optional[Sequence[str]]) -> Dict[str, Optional[Sequence[str]]]:
        """Returns scopes kwargs to pass to google-auth methods depending on the google-auth version"""

        scopes_kwargs = {}

        if _GOOGLE_AUTH_VERSION and (
            packaging.version.parse(_GOOGLE_AUTH_VERSION)
            >= packaging.version.parse("1.25.0")
        ):
            scopes_kwargs = {"scopes": scopes, "default_scopes": cls.AUTH_SCOPES}
        else:
            scopes_kwargs = {"scopes": scopes or cls.AUTH_SCOPES}

        return scopes_kwargs

    # TODO: Remove this function once google-api-core >= 1.26.0 is required
    @classmethod
    def _get_self_signed_jwt_kwargs(cls, host: str, scopes: Optional[Sequence[str]]) -> Dict[str, Union[Optional[Sequence[str]], str]]:
        """Returns kwargs to pass to grpc_helpers.create_channel depending on the google-api-core version"""

        self_signed_jwt_kwargs: Dict[str, Union[Optional[Sequence[str]], str]] = {}

        if _API_CORE_VERSION and (
            packaging.version.parse(_API_CORE_VERSION)
            >= packaging.version.parse("1.26.0")
        ):
            self_signed_jwt_kwargs["default_scopes"] = cls.AUTH_SCOPES
            self_signed_jwt_kwargs["scopes"] = scopes
            self_signed_jwt_kwargs["default_host"] = cls.DEFAULT_HOST
        else:
            self_signed_jwt_kwargs["scopes"] = scopes or cls.AUTH_SCOPES

        return self_signed_jwt_kwargs

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.create_reservation: gapic_v1.method.wrap_method(
                self.create_reservation,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_reservations: gapic_v1.method.wrap_method(
                self.list_reservations,
                default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_reservation: gapic_v1.method.wrap_method(
                self.get_reservation,
                default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_reservation: gapic_v1.method.wrap_method(
                self.delete_reservation,
                default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_reservation: gapic_v1.method.wrap_method(
                self.update_reservation,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_capacity_commitment: gapic_v1.method.wrap_method(
                self.create_capacity_commitment,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_capacity_commitments: gapic_v1.method.wrap_method(
                self.list_capacity_commitments,
                default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_capacity_commitment: gapic_v1.method.wrap_method(
                self.get_capacity_commitment,
                default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_capacity_commitment: gapic_v1.method.wrap_method(
                self.delete_capacity_commitment,
                default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_capacity_commitment: gapic_v1.method.wrap_method(
                self.update_capacity_commitment,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.split_capacity_commitment: gapic_v1.method.wrap_method(
                self.split_capacity_commitment,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.merge_capacity_commitments: gapic_v1.method.wrap_method(
                self.merge_capacity_commitments,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_assignment: gapic_v1.method.wrap_method(
                self.create_assignment,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_assignments: gapic_v1.method.wrap_method(
                self.list_assignments,
                default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_assignment: gapic_v1.method.wrap_method(
                self.delete_assignment,
                default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.search_assignments: gapic_v1.method.wrap_method(
                self.search_assignments,
                default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.move_assignment: gapic_v1.method.wrap_method(
                self.move_assignment,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_bi_reservation: gapic_v1.method.wrap_method(
                self.get_bi_reservation,
                default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_bi_reservation: gapic_v1.method.wrap_method(
                self.update_bi_reservation,
                default_timeout=60.0,
                client_info=client_info,
            ),
         }

    @property
    def create_reservation(self) -> Callable[
            [gcbr_reservation.CreateReservationRequest],
            Union[
                gcbr_reservation.Reservation,
                Awaitable[gcbr_reservation.Reservation]
            ]]:
        raise NotImplementedError()

    @property
    def list_reservations(self) -> Callable[
            [reservation.ListReservationsRequest],
            Union[
                reservation.ListReservationsResponse,
                Awaitable[reservation.ListReservationsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def get_reservation(self) -> Callable[
            [reservation.GetReservationRequest],
            Union[
                reservation.Reservation,
                Awaitable[reservation.Reservation]
            ]]:
        raise NotImplementedError()

    @property
    def delete_reservation(self) -> Callable[
            [reservation.DeleteReservationRequest],
            Union[
                empty.Empty,
                Awaitable[empty.Empty]
            ]]:
        raise NotImplementedError()

    @property
    def update_reservation(self) -> Callable[
            [gcbr_reservation.UpdateReservationRequest],
            Union[
                gcbr_reservation.Reservation,
                Awaitable[gcbr_reservation.Reservation]
            ]]:
        raise NotImplementedError()

    @property
    def create_capacity_commitment(self) -> Callable[
            [reservation.CreateCapacityCommitmentRequest],
            Union[
                reservation.CapacityCommitment,
                Awaitable[reservation.CapacityCommitment]
            ]]:
        raise NotImplementedError()

    @property
    def list_capacity_commitments(self) -> Callable[
            [reservation.ListCapacityCommitmentsRequest],
            Union[
                reservation.ListCapacityCommitmentsResponse,
                Awaitable[reservation.ListCapacityCommitmentsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def get_capacity_commitment(self) -> Callable[
            [reservation.GetCapacityCommitmentRequest],
            Union[
                reservation.CapacityCommitment,
                Awaitable[reservation.CapacityCommitment]
            ]]:
        raise NotImplementedError()

    @property
    def delete_capacity_commitment(self) -> Callable[
            [reservation.DeleteCapacityCommitmentRequest],
            Union[
                empty.Empty,
                Awaitable[empty.Empty]
            ]]:
        raise NotImplementedError()

    @property
    def update_capacity_commitment(self) -> Callable[
            [reservation.UpdateCapacityCommitmentRequest],
            Union[
                reservation.CapacityCommitment,
                Awaitable[reservation.CapacityCommitment]
            ]]:
        raise NotImplementedError()

    @property
    def split_capacity_commitment(self) -> Callable[
            [reservation.SplitCapacityCommitmentRequest],
            Union[
                reservation.SplitCapacityCommitmentResponse,
                Awaitable[reservation.SplitCapacityCommitmentResponse]
            ]]:
        raise NotImplementedError()

    @property
    def merge_capacity_commitments(self) -> Callable[
            [reservation.MergeCapacityCommitmentsRequest],
            Union[
                reservation.CapacityCommitment,
                Awaitable[reservation.CapacityCommitment]
            ]]:
        raise NotImplementedError()

    @property
    def create_assignment(self) -> Callable[
            [reservation.CreateAssignmentRequest],
            Union[
                reservation.Assignment,
                Awaitable[reservation.Assignment]
            ]]:
        raise NotImplementedError()

    @property
    def list_assignments(self) -> Callable[
            [reservation.ListAssignmentsRequest],
            Union[
                reservation.ListAssignmentsResponse,
                Awaitable[reservation.ListAssignmentsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def delete_assignment(self) -> Callable[
            [reservation.DeleteAssignmentRequest],
            Union[
                empty.Empty,
                Awaitable[empty.Empty]
            ]]:
        raise NotImplementedError()

    @property
    def search_assignments(self) -> Callable[
            [reservation.SearchAssignmentsRequest],
            Union[
                reservation.SearchAssignmentsResponse,
                Awaitable[reservation.SearchAssignmentsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def move_assignment(self) -> Callable[
            [reservation.MoveAssignmentRequest],
            Union[
                reservation.Assignment,
                Awaitable[reservation.Assignment]
            ]]:
        raise NotImplementedError()

    @property
    def get_bi_reservation(self) -> Callable[
            [reservation.GetBiReservationRequest],
            Union[
                reservation.BiReservation,
                Awaitable[reservation.BiReservation]
            ]]:
        raise NotImplementedError()

    @property
    def update_bi_reservation(self) -> Callable[
            [reservation.UpdateBiReservationRequest],
            Union[
                reservation.BiReservation,
                Awaitable[reservation.BiReservation]
            ]]:
        raise NotImplementedError()


__all__ = (
    'ReservationServiceTransport',
)