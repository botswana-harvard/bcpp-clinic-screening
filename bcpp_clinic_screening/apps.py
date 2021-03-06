from django.apps import AppConfig as DjangoApponfig

from datetime import datetime
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from dateutil.tz import gettz

from django.conf import settings

from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
from edc_appointment.facility import Facility
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
from edc_base.utils import get_utcnow
from edc_constants.constants import FAILED_ELIGIBILITY
from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
from edc_device.constants import CENTRAL_SERVER
from edc_identifier.apps import AppConfig as BaseEdcIdentifierAppConfig
from edc_map.apps import AppConfig as BaseEdcMapAppConfig
from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig
from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig, SubjectType, Cap
from edc_sync.apps import AppConfig as BaseEdcSyncAppConfig
from edc_sync_files.apps import AppConfig as BaseEdcSyncFilesAppConfig
from edc_timepoint.apps import AppConfig as BaseEdcTimepointAppConfig
from edc_timepoint.timepoint import Timepoint
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT


class AppConfig(DjangoApponfig):
    name = 'bcpp_clinic_screening'
    listboard_template_name = 'bcpp_clinic_screening/listboard.html'
    listboard_url_name = 'bcpp_clinic_screening:listboard_url'
    base_template_name = 'edc_base/base.html'
    url_namespace = 'bcpp_clinic_screening'  # FIXME: is this still neeed??
    admin_site_name = 'bcpp_clinic_screening_admin'

    eligibility_age_adult_lower = 18
    eligibility_age_adult_upper = 64
    eligibility_age_minor_lower = 16
    eligibility_age_minor_upper = 17


class EdcIdentifierAppConfig(BaseEdcIdentifierAppConfig):
    identifier_prefix = '066'


class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
    use_settings = True
    device_id = settings.DEVICE_ID
    device_role = settings.DEVICE_ROLE


class EdcMapAppConfig(BaseEdcMapAppConfig):
    verbose_name = 'BCPP Mappers'
    mapper_model = 'bcpp_clinic_screening.subjecteligibility'


class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
    protocol = 'BHP066'
    protocol_number = '066'
    protocol_name = 'BCPP Clinic'
    protocol_title = 'Botswana Combination Prevention Project'
    subject_types = [
        SubjectType('subject', 'Research Subject',
                    Cap(model_name='bcpp_clinic_subject.subjectconsent', max_subjects=9999)),
    ]
    study_open_datetime = datetime(2013, 10, 18, 0, 0, 0, tzinfo=gettz('UTC'))
    study_close_datetime = datetime(2018, 12, 1, 0, 0, 0, tzinfo=gettz('UTC'))

    @property
    def site_name(self):
        return 'test_community'

    @property
    def site_code(self):
        return '01'


class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
    reason_field = {'bcpp_clinic_subject.subjectvisit': 'reason'}
    create_on_reasons = [SCHEDULED, UNSCHEDULED]
    delete_on_reasons = [LOST_VISIT, FAILED_ELIGIBILITY]
    metadata_rules_enabled = True  # default


class EdcTimepointAppConfig(BaseEdcTimepointAppConfig):
    timepoints = [
        Timepoint(
            model='bcpp_clinic_subject.appointment',
            datetime_field='appt_datetime',
            status_field='appt_status',
            closed_status='DONE'
        ),
        Timepoint(
            model='bcpp_clinic_subject.historicalappointment',
            datetime_field='appt_datetime',
            status_field='appt_status',
            closed_status='DONE'
        ),
    ]


class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
    app_label = 'bcpp_clinic_subject'
    default_appt_type = 'clinic'
    facilities = {
        'clinic': Facility(name='clinic', days=[MO, TU, WE, TH, FR, SA, SU],
                           slots=[99999, 99999, 99999, 99999, 99999, 99999, 99999])}


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'Bcpp Clinic'
    institution = 'Botswana-Harvard AIDS Institute'
    copyright = '2013-{}'.format(get_utcnow().year)
    license = None


class EdcSyncAppConfig(BaseEdcSyncAppConfig):
    edc_sync_files_using = True
    role = CENTRAL_SERVER


class EdcSyncFilesAppConfig(BaseEdcSyncFilesAppConfig):
    edc_sync_files_using = True
    role = CENTRAL_SERVER
