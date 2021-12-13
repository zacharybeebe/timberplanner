from imports._imports_ import deepcopy
from models.orm import ORM


class Presale(ORM):
    args = {
        'ref': 'INTEGER',
        'sale_ref': 'INTEGER',
        'initial_map': 'INTEGER',
        'specialist_remote_review_requested': 'INTEGER',
        'access_assessment': 'INTEGER',
        'geology_assessment': 'INTEGER',
        'ecological_assessment': 'INTEGER',
        'archaeological_assessment': 'INTEGER',
        'rfrs_assessment': 'INTEGER',
        'survey_assessment': 'INTEGER',
        'survey_requested': 'INTEGER',

        'haul_route_recon': 'INTEGER',
        'stream_typing': 'INTEGER',
        'wetland_typing': 'INTEGER',
        'rfrs_plots': 'INTEGER',
        'rfrs_thinning_rx': 'INTEGER',
        'field_with_geologist': 'INTEGER',
        'field_with_biologist': 'INTEGER',
        'field_with_archaeologist': 'INTEGER',
        'preliminary_road_layout': 'INTEGER',
        'boundary_layout': 'INTEGER',
        'leave_tree_layout': 'INTEGER',
        'traverse_roads': 'INTEGER',

        'road_design': 'INTEGER',
        'road_plan': 'INTEGER',
        'final_spatial_lrm': 'INTEGER',
        'fma_silviculture_lrm': 'INTEGER',
        'pre_cruise_narrative': 'INTEGER',
        'final_maps': 'INTEGER',
        'contract_documents': 'INTEGER',
        'fpa_documents': 'INTEGER',
        'sepa_documents': 'INTEGER'
    }

    exclude = (
        'ref',
        'db',
        'conn',
        'cur',
        'info'
    )

    primary_key = 'ref'

    foreign_key = ('sale_ref', 'sales', 'ref')

    def __init__(self, db=None, ref=None, sale_ref=None, initial_map=0, specialist_remote_review_requested=0, access_assessment=0,
                 geology_assessment=0, ecological_assessment=0, archaeological_assessment=0, rfrs_assessment=0, survey_assessment=0,
                 survey_requested=0, haul_route_recon=0, stream_typing=0, wetland_typing=0, rfrs_plots=0, rfrs_thinning_rx=0,
                 field_with_geologist=0, field_with_biologist=0, field_with_archaeologist=0, preliminary_road_layout=0, boundary_layout=0,
                 leave_tree_layout=0, traverse_roads=0, road_design=0, road_plan=0, final_spatial_lrm=0, fma_silviculture_lrm=0,
                 pre_cruise_narrative=0, final_maps=0, contract_documents=0, fpa_documents=0, sepa_documents=0):
        super().__init__(db, ref)
        self.sale_ref = sale_ref
        self.initial_map = initial_map
        self.specialist_remote_review_requested = specialist_remote_review_requested
        self.access_assessment = access_assessment
        self.geology_assessment = geology_assessment
        self.ecological_assessment = ecological_assessment
        self.archaeological_assessment = archaeological_assessment
        self.rfrs_assessment = rfrs_assessment
        self.survey_assessment = survey_assessment
        self.survey_requested = survey_requested
        self.haul_route_recon = haul_route_recon
        self.stream_typing = stream_typing
        self.wetland_typing = wetland_typing
        self.rfrs_plots = rfrs_plots
        self.rfrs_thinning_rx = rfrs_thinning_rx
        self.field_with_geologist = field_with_geologist
        self.field_with_biologist = field_with_biologist
        self.field_with_archaeologist = field_with_archaeologist
        self.preliminary_road_layout = preliminary_road_layout
        self.boundary_layout = boundary_layout
        self.leave_tree_layout = leave_tree_layout
        self.traverse_roads = traverse_roads
        self.road_design = road_design
        self.road_plan = road_plan
        self.final_spatial_lrm = final_spatial_lrm
        self.fma_silviculture_lrm = fma_silviculture_lrm
        self.pre_cruise_narrative = pre_cruise_narrative
        self.final_maps = final_maps
        self.contract_documents = contract_documents
        self.fpa_documents = fpa_documents
        self.sepa_documents = sepa_documents

        self.info = None
        self.set_info()

    def set_info(self):
        self.info = {' '.join([i.capitalize() for i in key.split('_')]): self.__dict__[key]
                     for key in self.__dict__ if key in self.args and key not in ['ref', 'sale_ref']}
